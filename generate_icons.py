from PIL import Image, ImageDraw, ImageFont
import os

sizes = [16, 48, 128]
bg_color = (76, 175, 80)  # #4CAF50
text_color = (255, 255, 255)  # White

for size in sizes:
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw rounded rectangle background
    if size > 16:
        radius = size // 10
        draw.rounded_rectangle([(0, 0), (size-1, size-1)], radius=radius, fill=bg_color)
    
    # Draw text
    font_size = int(size * 0.6)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        font = ImageFont.load_default()
    
    text = "F"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - bbox[1]
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    img.save(f"chrome-extension/icon{size}.png")

print("Icons generated successfully!")