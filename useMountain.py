"""
CMPT 306 Fall 2025
Final Project: Mountain Paths
    GeoTiff downloaded from The National Map Downloader: https://apps.nationalmap.gov/downloader/
    The dataset selected for my files are 1-meter DEM from the Elevation Products (3D Elevation Program Products and Services) data section.
@author Heidi Andre
"""
import rasterio
import numpy as np
from heapq import heappush, heappop
import drawPath as draw
import matplotlib.pyplot as plt
import argparse

class Node():
    """
    cost_from_start - the cost of reaching this node from the starting node
    state - the state (row,col)
    parent - the parent node of this node, default as None
    """
    def __init__(self, state, cost_from_start, parent = None):
        self.state = state
        self.parent = parent
        self.cost_from_start = cost_from_start

class useMountain():

    def __init__(self, file, algorithm):
        """
        Opening and reading GeoTiff file.

        Args:
            file: The GeoTiff filepath.
            algorithm: The algorithm being used. Either Greedy or A*.
        """
        try:
            with rasterio.open(file) as dataset:
                self.elevation_data = dataset.read(1)
                self.file = file
                self.profile = dataset.profile

                self.height, self.width = self.elevation_data.shape
                self.visited = {}
                self.path = []
                self.algorithm = algorithm
                self.middle = self.height//2
                self.low_left = np.argmin(self.elevation_data[:, 0])
                # Starting state is currently the lowest elevation point of the leftmost side.
                self.start = (self.low_left, 0)
                self.low_right = np.argmin(self.elevation_data[:, -1])


                # Goal state is set to be the lowest elevation point on the rightmost side.
                self.goal_state = (self.low_right, self.width - 1)

                # If there is missing data in the GeoTiff the value of that pixel the value would show as -999999.0.
                self.nodata = dataset.nodata
                # print("data read")

        except rasterio.RasterioIOError:
            print(f"Error: Could not open the file at {file}. Check the path.")


    def pixel_path(self, node):
        """
        Final pixel path based on the algorithm.
        Args:
            node: Last node in the path.
        Returns:
            array: Final path of pixels end to start.
        """
        while node.parent:
            self.path.append(node.state)
            node = node.parent
        self.path.append(self.start)
        # Debugging Statement
        # print('Found Path')
        return self.path

    def goal_test(self, current):
        """
        Checking if the current pixel is at the last column (rightmost) satisfying project requirements.
        Args:
            current: Current pixel (row, col).
        """
        if current[1] == self.goal_state[1]: return True

    def get_cost(self, current_state, next_state):
        """
        Getting cost from current pixel to next pixel.
        Args:
            current_state: Current pixel (row, col).
            next_state: Next pixel (row, col).
        Returns:
            int: Absolute value of the elevation difference between current pixel and next pixel.
        """
        return abs(self.elevation_data[current_state[0], current_state[1]] - self.elevation_data[next_state[0], next_state[1]])

    def get_successors(self, current):
        """
        Getting next possible pixels with priority towards moving forward.
        Args:
            current: Current pixel (row, col).
        Returns:
            successors: List of next possible pixels and their priority.
        """
        successors = []
        y = current[0]
        x = current[1]


        moves = [
            ((0, 1), 0),   # Forward, highest priority
            ((-1, 1), 1),  # Up, second priority
            ((1, 1), 1)    # Down, second priority
        ]

        for move, move_priority in moves:
            test_y = y + move[0]
            test_x = x + move[1]

            # Boundary Checking
            if 0 <= test_y < self.height and 0 <= test_x < self.width:
                successors.append(((test_y, test_x), move_priority))
        return successors

    def priority(self, node):
        """
        Finding the priority value for the current node based on algorithm.
        Args:
            node: Most recent node.
        Returns:
            int: Priority value based on algorithm specification.
        """
        value = 0
        if self.algorithm == 'Greedy':
            value = self.heuristics(node.state)
        elif self.algorithm == 'AStar':
            value = self.heuristics(node.state) + node.cost_from_start
        return value

    def heuristics(self, state):
        """
        Using Manhattan distance calculation to find the heuristic value of pixel.
        Args:
            state: Current pixel (row,col).
        Returns:
            int: Heuristic value.
        """
        current_elev = self.elevation_data[state[0], state[1]]
        goal_elev = self.elevation_data[self.goal_state[0], self.goal_state[1]]
        elev_diff = abs(current_elev - goal_elev)

        # Added col_diff to prevent infinite/long run times.
        col_diff = abs(state[1] - (self.width - 1))

        return elev_diff + (1 * col_diff)

    def solve(self):
        """
        Finding path from start to then rightmost column.
        """
        if self.goal_test(self.start): return
        fringe = []
        state = self.start
        node = Node(state, 0, None)
        self.visited[state] = node
        count = 0

        heappush(fringe, (self.priority(node), count, 0, node))

        while fringe:
            current_priority, _, _, current_node = heappop(fringe)
            current_state = current_node.state

            if current_node.cost_from_start > self.visited[current_state].cost_from_start:
                continue

            if self.goal_test(current_state):
                # Debugging Statement
                # print("Goal Reached.")
                return self.pixel_path(current_node)

            for step, direction_priority in self.get_successors(current_state):

                next_cost = current_node.cost_from_start + self.get_cost(current_state, step)
                next_node = Node(step, next_cost, current_node)

                if step not in self.visited:
                    self.visited[step] = next_node
                    # print(step)
                    count += 1
                    heappush(fringe, (self.priority(next_node), count, direction_priority, next_node))


                elif next_cost < self.visited[step].cost_from_start:
                    self.visited[step] = next_node
                    # print(step)
                    count += 1
                    heappush(fringe, (self.priority(next_node), count, direction_priority, next_node))



    def greyscale(self):
        """
        Visualizing GeoTiff image in greyscale. Darker shades are lower elevation ranges, lighter shades are higher elevation ranges.
        """
        # Handling if there is missing data.
        if self.nodata is not None:
            valid_mask = (self.elevation_data != self.nodata)
            min_elev = self.elevation_data[valid_mask].min()
            max_elev = self.elevation_data[valid_mask].max()
        else:
            min_elev = self.elevation_data.min()
            max_elev = self.elevation_data.max()

        # Checking if there is no elevation change. Output will be a full white image.
        if max_elev == min_elev:
            grayscale_image = np.full(self.elevation_data.shape, 255, dtype=np.uint8)
        else:
            normalized_data = (self.elevation_data - min_elev) / (max_elev - min_elev)
            grayscale_image = (normalized_data * 255).astype(np.uint8)

        # Missing data will be black
        if self.nodata is not None:
            grayscale_image[~valid_mask] = 0

        # Image output being saved in same folder as original file
        output_path = 'grayscale_' + self.file
        if output_path:

            self.profile.update(
                dtype=rasterio.uint8,
                count=1,
                nodata=None
            )

            with rasterio.open(output_path, 'w', **self.profile) as dst:
                dst.write(grayscale_image, 1)
            print(f"Successfully saved grayscale GeoTIFF to: {output_path}")

            # Set to False. True will display elevation map with legend.
            show_plot = False
            if show_plot:
                plt.figure(figsize=(8, 8))
                plt.imshow(grayscale_image, cmap='gray')
                plt.suptitle('Grayscale Elevation Map (Min=Black, Max=White)')
                plt.title(f'Max Elevation: {max_elev}\nMin Elevation: {min_elev}')
                plt.colorbar(label='Pixel Value (0=Black, 255=White)')
                plt.show()
        return output_path

if __name__ == "__main__":
    algorithms = ['Greedy', 'AStar']

    file = 'harvard.tif'
    path = useMountain(file, algorithms[0])
    final = path.solve()

    # Debugging Statement
    # print(final)

    grey = path.greyscale()

    # Debugging Statement
    # print(grey)

    draw.drawPath(grey, final, algorithms[0])
