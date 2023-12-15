from PIL import Image, ImageDraw
import numpy as np

# Load the uploaded image
image_path = 'li_pre.png'
image = Image.open(image_path)

# Define the size of the patches (16x16)
patch_size = 56

# Calculate the number of patches along width and height
num_patches_x = image.width // patch_size
num_patches_y = image.height // patch_size

# Create a copy of the image to draw the grid
image_with_grid = image.copy()
draw = ImageDraw.Draw(image_with_grid)

# Draw the grid lines on the image
for i in range(0, image.width, patch_size):
    line = ((i, 0), (i, image.height))
    draw.line(line, fill="black")

for i in range(0, image.height, patch_size):
    line = ((0, i), (image.width, i))
    draw.line(line, fill="black")

# Save the image with the grid
grid_image_path = 'li_with_grid.png'
image_with_grid.save(grid_image_path)

# Now, let's cut the image into 16x16 patches
patches = []

for i in range(num_patches_y):
    for j in range(num_patches_x):
        # Calculate the bounding box of the current patch
        left = j * patch_size
        upper = i * patch_size
        right = left + patch_size
        lower = upper + patch_size
        
        # Extract the patch from the image
        patch = image.crop((left, upper, right, lower))
        patches.append(patch)

# Save the patches to disk and store their file paths
patch_file_paths = []

for idx, patch in enumerate(patches):
    patch_path = f'patch/patch_{idx}.png'
    patch.save(patch_path)
    patch_file_paths.append(patch_path)

# Return the image with grid and the paths to the saved patches
grid_image_path, patch_file_paths, len(patches)
