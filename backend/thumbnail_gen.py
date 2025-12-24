from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
import requests
from io import BytesIO

def generate_gradient():
    """Generates a random attractive gradient."""
    colors = [
        (255, 107, 107), (78, 205, 196), (69, 183, 209), (150, 201, 61),
        (249, 212, 35), (255, 159, 67), (84, 160, 255), (95, 39, 205)
    ]
    c1 = random.choice(colors)
    c2 = random.choice(colors)
    return c1, c2

def create_gradient_image(width, height, c1, c2):
    base = Image.new('RGB', (width, height), c1)
    top = Image.new('RGB', (width, height), c2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        for x in range(width):
            mask_data.append(int(255 * (y / height)))
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def download_image(url):
    """Downloads an image from a URL and returns a PIL Image object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Failed to download thumbnail image: {e}")
        return None

def generate_thumbnail(text, filename="thumbnail.png", bg_image_url=None):
    """
    Generates a thumbnail with text overlay.
    If bg_image_url is provided, it tries to use it as background.
    """
    website_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    public_dir = os.path.join(website_root, "public")
    
    # Ensure public dir exists
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)

    width, height = 1200, 630
    
    # 1. Prepare Background
    img = None
    is_photo = False

    if bg_image_url:
        print(f"Attempting to use background image: {bg_image_url}")
        downloaded_img = download_image(bg_image_url)
        if downloaded_img:
            # Resize and Crop to fill (cover)
            img_ratio = downloaded_img.width / downloaded_img.height
            target_ratio = width / height
            
            if img_ratio > target_ratio:
                # Image is wider: fit height
                new_height = height
                new_width = int(new_height * img_ratio)
            else:
                # Image is taller: fit width
                new_width = width
                new_height = int(new_width / img_ratio)
                
            downloaded_img = downloaded_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Center crop
            left = (new_width - width) / 2
            top = (new_height - height) / 2
            img = downloaded_img.crop((left, top, left + width, top + height))
            img = img.convert('RGB')
            is_photo = True
            
            # NO OVERLAY, NO TEXT for photos as requested
            
    if img is None:
        # Fallback to gradient
        c1, c2 = generate_gradient()
        img = create_gradient_image(width, height, c1, c2)
        is_photo = False

    # 2. Draw Text (ONLY if it's a gradient fallback, NOT on photos)
    if not is_photo:
        draw = ImageDraw.Draw(img)
        # Try to find a font (fallback to default if not found)
        # Windows paths
        font_paths = [
            "C:\\Windows\\Fonts\\meiryo.ttc",
            "C:\\Windows\\Fonts\\msgothic.ttc",
            "arial.ttf"
        ]
        font = None
        for path in font_paths:
            try:
                font = ImageFont.truetype(path, 80)
                break
            except:
                continue
        if not font:
            font = ImageFont.load_default()

        # Wrap text
        lines = []
        current_line = ""
        # Very simple Japanese wrapping (approx 10 chars per line for 80px font on 1200px width? No, more like 15)
        chars_per_line = 14
        for i in range(0, len(text), chars_per_line):
            lines.append(text[i:i+chars_per_line])
            
        # Draw Lines Centered
        total_height = len(lines) * 90 # line height
        start_y = (height - total_height) / 2
        
        for i, line in enumerate(lines):
            # Calculate text width (rudimentary)
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) / 2
            y = start_y + i * 90
            
            # Shadow/Outline
            shadow_offset = 3
            draw.text((x+shadow_offset, y+shadow_offset), line, font=font, fill="black")
            
            # Main Text
            draw.text((x, y), line, font=font, fill="white")

    # Save
    save_path = os.path.join(public_dir, filename)
    img.save(save_path)
    
    # Return relative URL
    return f"/{filename}"

if __name__ == "__main__":
    # Test with a dummy image (placehold.co)
    test_url = "https://images.unsplash.com/photo-1543852786-1cf6624b9987?q=80&w=1200" # Cat image
    generate_thumbnail("This text should NOT appear", "test_clean_thumb.png", bg_image_url=test_url)
    generate_thumbnail("Test Gradient", "test_gradient_thumb.png") # Fallback test
