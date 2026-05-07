from collections import deque

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = set()
        self.parent = {}


    def solve_maze(self, start, end):
        queue = deque([start])
        self.visited.add(start)
        self.parent[start] = None

        h, w = self.maze.shape

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                return self.reconstruct_path(end)

            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
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