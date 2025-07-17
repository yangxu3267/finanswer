#!/usr/bin/env python3
"""
创建 FinKnows Chrome 扩展图标
使用 PIL 生成不同尺寸的图标
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """创建指定尺寸的图标"""
    # 创建画布
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 计算字体大小
    font_size = int(size * 0.4)
    
    # 创建渐变背景
    for i in range(size):
        alpha = int(255 * (1 - i / size))
        color = (76, 222, 128, alpha)  # 绿色渐变
        draw.line([(0, i), (size, i)], fill=color)
    
    # 添加圆形背景
    circle_radius = int(size * 0.35)
    circle_center = size // 2
    circle_bbox = [
        circle_center - circle_radius,
        circle_center - circle_radius,
        circle_center + circle_radius,
        circle_center + circle_radius
    ]
    draw.ellipse(circle_bbox, fill=(24, 24, 28, 200))
    
    # 添加文字
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
    except:
        # 使用默认字体
        font = ImageFont.load_default()
    
    # 绘制 "FK" 文字
    text = "FK"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2
    
    # 绘制文字阴影
    draw.text((text_x + 2, text_y + 2), text, font=font, fill=(0, 0, 0, 100))
    # 绘制主文字
    draw.text((text_x, text_y), text, font=font, fill=(76, 222, 128, 255))
    
    # 保存图标
    img.save(filename, 'PNG')
    print(f"✅ 创建图标: {filename} ({size}x{size})")

def main():
    """主函数"""
    print("🎨 创建 FinKnows 图标...")
    
    # 确保 icons 目录存在
    if not os.path.exists('icons'):
        os.makedirs('icons')
    
    # 创建不同尺寸的图标
    icon_sizes = [16, 32, 48, 128]
    
    for size in icon_sizes:
        filename = f"icons/icon{size}.png"
        create_icon(size, filename)
    
    print("🎉 所有图标创建完成！")
    print("📁 图标文件保存在 icons/ 目录中")

if __name__ == "__main__":
    main() 