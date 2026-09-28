import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"PAGE LOG: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"PAGE ERROR: {exc}"))
        print("Navigating...")
        await page.goto("http://localhost:9876/projects/flight-tracker-widget/index.html", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        counts = await page.evaluate("""() => {
            return {
                aircraft: document.querySelectorAll('.aircraft-marker').length,
                leaflet_marker: document.querySelectorAll('.leaflet-marker-icon').length,
                mapHtml: document.getElementById('map').innerHTML.length
            }
        }""")
        print(f"Counts: {counts}")
        
        # take screenshot
        await page.screenshot(path="public/demos/debug.png")
        print("Done")
        await browser.close()

asyncio.run(main())
