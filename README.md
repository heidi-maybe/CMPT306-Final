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
### drawPath.py
### harvard_elevation.pdf
### wasatch_elevation.pdf
### zirkel_elevation.pdf
### CMPT 306 Mountain Paths

## Known Issues and Limitations
Changing the targeted GeoTiff file, algorithm used, and returned file names all have to be edited manually in the code.
