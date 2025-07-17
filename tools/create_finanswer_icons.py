#!/usr/bin/env python3
"""
Finanswer Icon Generator
Creates modern, professional icons for the Finanswer Chrome extension
"""

from PIL import Image, ImageDraw, ImageFont
import os

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_icon(size, text="FA", bg_color="#1a1a1a", primary_color="#00d4aa", secondary_color="#ff6b35"):
    """Create a modern icon with the given size and colors"""
    
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Convert colors
    bg_rgb = hex_to_rgb(bg_color)
    primary_rgb = hex_to_rgb(primary_color)
    secondary_rgb = hex_to_rgb(secondary_color)
    
    # Calculate dimensions
    padding = max(2, size // 12)
    inner_size = size - (padding * 2)
    
    # Draw main background circle
    draw.ellipse([padding, padding, size - padding, size - padding], 
                fill=bg_rgb)
    
    # Draw accent circle (top right)
    accent_size = max(4, size // 6)
    accent_x = size - padding - accent_size
    accent_y = padding
    draw.ellipse([accent_x, accent_y, accent_x + accent_size, accent_y + accent_size], 
                fill=primary_rgb)
    
    # Draw chart bars at bottom
    if size >= 32:  # Only draw chart for larger icons
        chart_width = size // 2
        chart_height = size // 8
        chart_x = (size - chart_width) // 2
        chart_y = size - padding - chart_height - size // 12
        
        # Three bars with increasing heights
        bar_width = chart_width // 4
        bar_spacing = bar_width // 3
        
        for i in range(3):
            bar_x = chart_x + (i * (bar_width + bar_spacing))
            bar_height = chart_height * (0.5 + (i * 0.25))
            bar_y = chart_y + chart_height - bar_height
            
            # Create gradient effect
            for j in range(int(bar_height)):
                alpha = max(100, 255 - (j * 3))
                color = (*secondary_rgb, alpha)
                draw.rectangle([bar_x, bar_y + j, bar_x + bar_width - 1, bar_y + j], 
                              fill=color)
    
    # Add text "FA"
    try:
        # Try to use a system font
        font_size = max(8, size // 3)
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Calculate text position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - size // 16  # Slightly above center
    
    # Draw text with shadow effect
    shadow_offset = max(1, size // 32)
    draw.text((text_x + shadow_offset, text_y + shadow_offset), text, 
              font=font, fill=(0, 0, 0, 150))
    draw.text((text_x, text_y), text, font=font, fill=primary_rgb)
    
    return img

def create_icon_set():
    """Create icons in all required sizes for Chrome extension"""
    
    sizes = [16, 32, 48, 128]
    icons_dir = "extension/icons"
    
    # Create icons directory if it doesn't exist
    os.makedirs(icons_dir, exist_ok=True)
    
    print("🎨 Creating Finanswer icons...")
    
    for size in sizes:
        icon = create_icon(size)
        filename = f"{icons_dir}/icon{size}.png"
        icon.save(filename, "PNG")
        print(f"✅ Created {filename} ({size}x{size})")
    
    print("\n🎉 All icons created successfully!")
    print(f"📁 Icons saved in: {icons_dir}/")
    
    # Create a preview image
    preview = create_icon(256)
    preview.save(f"{icons_dir}/preview.png", "PNG")
    print(f"📸 Preview saved as: {icons_dir}/preview.png")

if __name__ == "__main__":
    create_icon_set() 