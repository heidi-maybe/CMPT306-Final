# Mountain Paths Project
## Brief Description
Final project for Westminster CMPT 306 Fall Semester 2025. The goal of this project is to use elevation data from a mountain region and find a path across that region that equates to the least amount of elevation change. This program takes a GeoTiff file and uses either the Greedy or A* algorithms to determine the path from the left side of the image to the right side. Elevation data is estracted from the GeoTiff using rasterio and that data is manipulated using numpy. The goal condition for the path is to reach the lowest elevation point on the right side of the image. The goal test condition returns true if the path that the algorithm determines reaches the right most side of the image.

Once the path has been determined the GeoTiff is converted into a grayscale image where there the lowest elevation in the given region is black and the highest elevation is white. The color of the path is determined by the algorithm that is used, yellow is A* and red is Greedy.

## Author
Heidi Andre

## Language
Python

## Files
This repository contains useMountain.py, drawPath.py, harvard_elevation.pdf, wasatch_elevation.pdf, zirkel_elevation.pdf, and CMPT 306 Mountain Paths powerpoint file. 

### useMountain.py
useMountain.py handles the estraction of the elevation data using rasterio and finds the path based on the designated algorithm. Starting row on the leftmost side of the image is determined by `self.start` in the `__init__` method for useMountain class. Currently the middle pixel of the image (`self.middle`) and the lowest elevation point (`self.low_left`) are available to switch out. This file also handles the conversion to a grayscale image and if `show_plot = True` a grayscale image with a legend is also produced. 255 pixel value is white meaning the highest elevation in the given region. A pixel value of 0 is black meaning the lowest elevation in the given region. 

### drawPath.py
drawPath.py handles the actual drawing of the path that useMoutain.py found. Using PIL the grayscale image and pixel path that useMountain.py produced the program follows the path changing the color of the pixels to the one that corresponds with the algorithm that was used.

### harvard_elevation.pdf
harvard_elevation.pdf is a pdf file that contains all of the results for a section of Harvard mountain in Colorado. For this dataset the top left corners coordinates are 38.931 °N, 106.384 °W and the bottom right corner coordinates are 38.840 °N, 106.267 °W. The first page in the file is a page of contents explaining each of the following pages. 

### wasatch_elevation.pdf
wasatch_elevation.pdf is a pdf file that contains all of the results for a section of the Wasatch mountain range in Utah. For this dataset the top left corners coordinates are 40.469 °N 111.472 °W and the bottom right corner coordinates are 40.379 ° N 111.353 °W. The first page in the file is a page of contents explaining each of the following pages. 

### zirkel_elevation.pdf
zirkel_elevation.pdf is a pdf file that contains all of the results for a section of the Mount Zirkel Wilderness in Colorado. For this dataset the top left corners coordinates are 40.729 °N 106.776° W and the bottom right corner coordinates are 40.637 °N 106.655 °W. The first page in the file is a page of contents explaining each of the following pages. 

### CMPT 306 Mountain Paths
This is the powerpoint presentation that I put together to present to the class at the end of the semester. This contains instructions on how to get the GeoTiff files from the USGS National Map Downloader.

## Known Issues and Limitations
Changing the targeted GeoTiff file, algorithm used, starting point on the left side, and returned file names all have to be edited manually in the code.
