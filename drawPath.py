"""
CMPT 306 Fall 2025
Final Project: Mountain Paths
    GeoTiff downloaded from The National Map Downloader: https://apps.nationalmap.gov/downloader/
    The dataset selected for my files are 1-meter DEM from the Elevation Products (3D Elevation Program Products and Services) data section.
    This takes the array of pixel coordinates from useMountain.py and draws colored lines based on the algorithm method used.
@author Heidi Andre
"""
from PIL import Image, ImageDraw

def drawPath(image, path, color):

    img = Image.open(image)
    pixel_path = path

    # Convert to RGB to see the color of drawn path.
    img_rgb = img.convert('RGB')
    # Switching from (row, col) to (col, row) for PIL
    x_y_path = [(x, y) for y, x in pixel_path]

    draw = ImageDraw.Draw(img_rgb)

    if color == 'Greedy':
        line_color = 'red'
    elif color == 'AStar':
        line_color = 'yellow'
    line = 40

    draw.line(x_y_path, fill=line_color, width=line)

    img_rgb.save('path_'+ color + '_' + image)
