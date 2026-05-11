from util.maze_solver import MazeSolver
from util.camera_controller import CameraController
from util.image_preprocessor import ImagePreprocessor
from util.path_visualizer import PathVisualizer

if __name__ == "__main__":
    camera = CameraController()
    preprocessor = ImagePreprocessor()

    frame = camera.get_frame()
    h, w = frame.shape[:2]
    visualizer = PathVisualizer(h, w)

    while True:
        try:
            frame = camera.get_frame()
            display_frame = frame.copy()
            gray, blurred, binary = preprocessor.preprocess(frame)
            contours = preprocessor.find_contours(blurred)

            #preprocessor.show_image("Binary Image", binary)
            #preprocessor.show_image("Blurred Image", blurred)

            if contours is not None:
                masked_image = preprocessor.apply_mask(frame, contours)
                warped_maze = preprocessor.four_point_transform(binary, contours)
                #preprocessor.show_image("Warped Maze", warped_maze)

                cleaned_maze = preprocessor.clean_binary(warped_maze)
                #preprocessor.show_image("Cleaned Maze", cleaned_maze)

                bordered_maze = preprocessor.add_border_walls(cleaned_maze)
                #preprocessor.show_image("Bordered Maze", bordered_maze)

                start, end = preprocessor.find_start_end_hsv(bordered_maze)

                grid = preprocessor.to_grid(bordered_maze)
                #preprocessor.show_image("Grid", grid * 255)


                solver = MazeSolver(grid)
                path = solver.solve_maze(start, end)
                if path is not None:
                    original_path = [preprocessor.warp_to_original(p) for p in path]
                    visualizer.draw_path(display_frame, original_path)

                else:
                    print("No path found in the maze.")
                
            key = visualizer.show("Camera Feed", display_frame)
            visualizer.to_video(display_frame)
            if key == ord('q'):
                break

        except Exception as e:
            print(f"Error: {e}")
            visualizer.out.release()   
            camera.cap.release()
            visualizer.destroy_all_windows()
            