import os
from PIL import Image, ImageDraw, ImageFont

def create_slide(text_lines, filename, size=(800, 450)):
    # Dark cosmic blue background
    img = Image.new('RGB', size, color='#060809')
    draw = ImageDraw.Draw(img)
    
    # Try to load a nice font, fallback to default
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 36)
        font_text = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    y_offset = size[1] // 3 - 20
    for i, line in enumerate(text_lines):
        font = font_title if i == 0 else font_text
        # Basic text centering
        text_bbox = draw.textbbox((0, 0), line, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]
        x_offset = (size[0] - text_w) // 2
        
        # Color: celestial blue for title, starlight mist for text
        color = "#72A1DE" if i == 0 else "#CAD6F2"
        draw.text((x_offset, y_offset), line, font=font, fill=color)
        y_offset += text_h + 20

    img.save(filename)

create_slide(
    ["RJ Airplane Tracker", "Native Windows Flight Radar"],
    "slide1.png"
)

create_slide(
    ["How it Works", "Haversine Spatial Geofencing", "Live ADS-B Telemetry via OpenSky"],
    "slide2.png"
)

create_slide(
    ["Key Features", "Windows 11 Toast Notifications", "GPU-Accelerated Leaflet Mapping"],
    "slide3.png"
)

print("Slides resized successfully.")
