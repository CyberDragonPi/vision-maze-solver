from collections import deque
from multiprocessing.util import debug
import numpy
import cv2

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = set()
        self.parent = {}


    def _convolute_maze(self, kernel_size=3):
        kernel = numpy.ones((kernel_size, kernel_size), dtype=numpy.uint8)

        summed = cv2.filter2D(self.maze, -1, kernel)
        safe_maze = (summed == 9).astype(numpy.uint8)
        return safe_maze

    def solve_maze(self, start, end):
        safe_maze = self._convolute_maze()

        queue = deque([start])
        self.visited.add(start)
        self.parent[start] = None

        h, w = safe_maze.shape
        
        """
        print(
        f"Solving maze of size {h}x{w} "
        f"from {start} to {end}. "
        f"Values: {numpy.unique(safe_maze)}"
        )
        """
        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                return self.reconstruct_path(end)

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < h and 0 <= ny < w:
                    if (nx, ny) not in self.visited and self.maze[nx, ny] == 1:
                        self.visited.add((nx, ny))
                        self.parent[(nx, ny)] = (x, y)
                        queue.append((nx, ny))
        return None


    def reconstruct_path(self, end):
        path = []
        current = end

        while current is not None:
            path.append(current)
            current = self.parent[current]

        path.reverse()
        return path