from PIL import Image
import os

def crop_center_square_face(image_path, output_path):
    try:
        img = Image.open(image_path)
        img = img.convert("RGBA")
        
        # Get bounding box of non-transparent area
        bbox = img.getbbox()
        if not bbox:
            print("Image is empty")
            return

        # Crop to content
        img_content = img.crop(bbox)
        
        # Assume face is at the top. 
        # We want a square crop from the top-center of the content.
        width, height = img_content.size
        
        # Determine square size - usually the width of the character
        # But if it's very tall, width is good.
        square_size = min(width, height)
        
        # Calculate coordinates for top-center crop
        left = (width - square_size) // 2
        top = 0 # Top alignment for head
        right = left + square_size
        bottom = square_size
        
        # Crop the face/head area
        face_img = img_content.crop((left, top, right, bottom))
        
        # Resize to standard icon size (256x256 is good for high res favicon)
        face_img = face_img.resize((256, 256), Image.Resampling.LANCZOS)
        
        face_img.save(output_path)
        print(f"Successfully created favicon at {output_path}")
        
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    # Paths assuming script is run from backend or root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "public", "mascot_cat.png")
    output_path = os.path.join(base_dir, "public", "favicon.png")
    
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    
    crop_center_square_face(input_path, output_path)
