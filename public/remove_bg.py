from PIL import Image

def remove_background(path):
    print(f"Processing {path}...")
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    # Heuristic: The background is a checkerboard.
    # We will assume the top-left corner is background.
    
    bg_colors = set()
    
    # Scan edges to find the palette of the background
    for x in range(0, width, 5):
        bg_colors.add(pixels[x, 0])
        bg_colors.add(pixels[x, height-1])
        
    for y in range(0, height, 5):
        bg_colors.add(pixels[0, y])
        bg_colors.add(pixels[width-1, y])
        
    # Filter bg_colors to only include "gray/white"ish things
    final_bg_colors = set()
    for c in bg_colors:
        # If it's pure gray or white
        if abs(c[0] - c[1]) < 15 and abs(c[1] - c[2]) < 15:
             if c[3] == 255: # Fully opaque
                 final_bg_colors.add(c)
    
    # Explicitly add common checkerboard colors
    final_bg_colors.add((255, 255, 255, 255)) # White
    final_bg_colors.add((254, 254, 254, 255)) # Near White
    final_bg_colors.add((235, 235, 235, 255)) # Light Gray
    final_bg_colors.add((204, 204, 204, 255)) # Medium Gray
    final_bg_colors.add((191, 191, 191, 255)) # Checkerboard Gray

    # Floodfill from corners
    queue = [(0,0), (width-1, 0), (0, height-1), (width-1, height-1)]
    visited = set(queue)
    
    removed_count = 0
    
    def matches_bg_set(pix, bg_set, tol=20):
        if pix[3] == 0: return True # pass through transparent
        for bg in bg_set:
            if abs(pix[0]-bg[0]) < tol and abs(pix[1]-bg[1]) < tol and abs(pix[2]-bg[2]) < tol:
                return True
        return False

    while queue:
        x, y = queue.pop(0)
        
        # Check current pixel
        if matches_bg_set(pixels[x,y], final_bg_colors):
            if pixels[x,y][3] != 0:
                pixels[x,y] = (0,0,0,0)
                removed_count += 1
            
            # Add neighbors
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        else:
            continue

    print(f"  Removed {removed_count} pixels.")
    img.save(path)

if __name__ == "__main__":
    remove_background('mascot_bunny.png')
