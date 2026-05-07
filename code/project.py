from maze_solver import MazeSolver
from camera_controller import CameraController
from image_preprocessor import ImagePreprocessor
from path_drawer import PathVisualizer
import cv2

if __name__ == "__main__":
    camera = CameraController()
    preprocessor = ImagePreprocessor() 

    try:
        gray, blurred, binary = preprocessor.preprocess()
        contours = preprocessor.find_contours(blurred)

        if contours is not None:
            warped_gray = preprocessor.four_point_transform(gray, contours)
            binary = preprocessor.to_binary(warped_gray)
            cleaned_binary = preprocessor.clean_binary(binary)
            bordered = preprocessor.add_border_walls(cleaned_binary) 

            grid = preprocessor.to_grid(bordered)
            maze_solver = MazeSolver(grid)
            start, end = preprocessor.find_start_end_points(grid)
            maze_solver.solve_maze(start, end)
            path = maze_solver.reconstruct_path(end)

            visualizer = PathVisualizer(warped_gray)
            path_image = visualizer.draw_path(path)
            visualizer.show()



    finally:
        camera.release()