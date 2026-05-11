# Vision-Based Maze Solver

A real-time computer vision system that detects, solves, and visualizes maze paths from live camera feed. The project combines classical image processing with graph search algorithms to automatically extract a maze structure and compute the shortest path between a start and end point.

---

## Features

-  Real-time camera input support (USB webcam)
- Automatic maze detection using contour extraction
- Perspective correction (four-point transform)
- Image preprocessing (adaptive thresholding, morphological operations)
- Automatic start/end detection using color segmentation (HSV filtering)
- Maze solving using Breadth-First Search (BFS)
- Path visualization on original image
- Optional video recording of the solving process

---

## How It Works

1. **Capture Frame**  
   The system reads frames from a live camera or image input.

2. **Maze Detection**  
   The largest contour is detected and approximated to isolate the maze.

3. **Perspective Correction**  
   A homography transform straightens the maze for processing.

4. **Preprocessing**  
   - Grayscale conversion  
   - Adaptive thresholding  
   - Morphological cleanup  

5. **Start/End Detection**  
   Uses HSV color filtering to locate red (start) and blue (end) markers.

6. **Pathfinding**  
   BFS is used to compute the shortest path in the grid representation.

7. **Visualization**  
   The solution path is drawn back onto the original image.

---

## 🛠️ Technologies Used

- Python
- OpenCV
- NumPy
- BFS Algorithm

---

## Project Structure
project/
├── code/
│ ├── project.py
│ ├── convert_maps_for_print.py
│ └── util/
│ ├── camera_controller.py
│ ├── maze_solver.py
│ ├── image_preprocessor.py
│ └── path_visualizer.py
├── examples/
│ ├── labirinto.jpg
│ ├── maze_output.avi
│ └── solved_maze.jpg
└── maps/
├── Day1_2.png
├── Day2_1.png
├── Day2_3.png
└── Day3_1.png
