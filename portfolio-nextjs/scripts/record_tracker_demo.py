"""
Playwright + FFmpeg: Record a clean LinkedIn demo video of the RJ Airplane Tracker.
No TTS, no voiceover, no script audio, no watermarks. Pure product demo.

Usage:
    python scripts/record_tracker_demo.py
"""

import asyncio
import os
import subprocess
import threading
import http.server
from pathlib import Path
from playwright.async_api import async_playwright


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_DIR = PROJECT_ROOT / "public"
OUTPUT_DIR = PROJECT_ROOT / "public" / "demos"
TRACKER_URL = "http://localhost:9876/projects/flight-tracker-widget/index.html"


def start_local_server(directory: Path, port: int = 9876):
    """Serve static files from the given directory on localhost."""
    os.chdir(str(directory))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *_: None  # silence logs
    server = http.server.HTTPServer(("localhost", port), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


async def record_demo():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Start local HTTP server for static files
    server = start_local_server(PUBLIC_DIR)
    print(f"Local server started on http://localhost:9876")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(OUTPUT_DIR),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = await context.new_page()

        print("Navigating to tracker...")
        await page.goto(TRACKER_URL, wait_until="networkidle")
        await page.wait_for_timeout(4000)  # let map + tiles render

        # --- Interaction sequence ---

        # 1. Let simulation flights populate
        print("Waiting for simulation flights...")
        await page.wait_for_timeout(4000)

        # 2. Toggle through radius options
        radius_buttons = await page.query_selector_all(".radius-btn")
        if len(radius_buttons) >= 1:
            print("Switching to 5 km radius...")
            await radius_buttons[0].click()
            await page.wait_for_timeout(3000)

        if len(radius_buttons) >= 3:
            print("Switching to 15 km radius...")
            await radius_buttons[2].click()
            await page.wait_for_timeout(3000)

        if len(radius_buttons) >= 2:
            print("Switching to 10 km radius...")
            await radius_buttons[1].click()
            await page.wait_for_timeout(3000)

        # 3. Click aircraft markers to open the info HUD card
        markers = await page.query_selector_all(".leaflet-marker-icon")
        if len(markers) >= 1:
            print(f"Clicking aircraft marker 1 of {len(markers)}...")
            await markers[0].click()
            await page.wait_for_timeout(4000)

        if len(markers) >= 2:
            print(f"Clicking aircraft marker 2...")
            await markers[1].click()
            await page.wait_for_timeout(4000)

        # 4. Toggle ground planes on
        ground_btn = await page.query_selector("#btn-ground")
        if ground_btn:
            print("Toggling ground planes ON...")
            await ground_btn.click()
            await page.wait_for_timeout(3000)

        # 5. Open notification settings panel
        settings_btn = await page.query_selector("#btn-settings")
        if settings_btn:
            print("Opening notification settings...")
            await settings_btn.click()
            await page.wait_for_timeout(3000)

        # 6. Close settings
        close_btn = await page.query_selector(".panel-close")
        if close_btn:
            print("Closing settings panel...")
            await close_btn.click()
            await page.wait_for_timeout(2000)

        # 7. Toggle ground planes off
        if ground_btn:
            print("Toggling ground planes OFF...")
            await ground_btn.click()
            await page.wait_for_timeout(2000)

        # 8. Click another aircraft if available
        markers = await page.query_selector_all(".leaflet-marker-icon")
        if len(markers) >= 3:
            print(f"Clicking aircraft marker 3...")
            await markers[2].click()
            await page.wait_for_timeout(4000)

        # 9. Final hold — let the radar run
        print("Final hold (5s)...")
        await page.wait_for_timeout(5000)

        # Close context to finalize video
        await context.close()
        await browser.close()

    server.shutdown()

    # --- Convert WebM to MP4 with FFmpeg ---
    webm_files = sorted(OUTPUT_DIR.glob("*.webm"), key=lambda f: f.stat().st_mtime)
    if not webm_files:
        print("ERROR: No WebM recording found.")
        return

    latest_webm = webm_files[-1]
    mp4_output = OUTPUT_DIR / "rj_flight_tracker_demo.mp4"

    print(f"\nConverting {latest_webm.name} -> rj_flight_tracker_demo.mp4 ...")
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-i", str(latest_webm),
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", "60",
        "-an",
        str(mp4_output),
    ]
    subprocess.run(ffmpeg_cmd, check=True)

    # Clean up intermediate WebM
    latest_webm.unlink(missing_ok=True)

    print(f"\nDONE! LinkedIn-ready video saved to:")
    print(f"   {mp4_output}")
    print(f"   Size: {mp4_output.stat().st_size / (1024*1024):.1f} MB")


if __name__ == "__main__":
    asyncio.run(record_demo())
