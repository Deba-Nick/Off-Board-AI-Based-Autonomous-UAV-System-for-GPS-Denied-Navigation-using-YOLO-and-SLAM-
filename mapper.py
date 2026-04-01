import cv2
import numpy as np
import os
from datetime import datetime

class FlightMapper:
    def __init__(self, save_dir="map", canvas_size=1000):
        """
        Initializes a blank 2D canvas for dead-reckoning navigation.
        canvas_size: 1000x1000 pixels. The drone starts dead center (500, 500).
        """
        self.save_dir = save_dir
        self.canvas_size = canvas_size
        self.center = (canvas_size // 2, canvas_size // 2)
        self.path = [self.center]  # List of (X, Y) coordinates, starting at center
        
        # Mapping scale: How many pixels on the map equal one movement command?
        # A 200ms swipe might equal 10 pixels on our map.
        self.scale = 10 

    def update_position(self, direction):
        """
        Updates the drone's estimated 2D position based on movement commands.
        """
        last_x, last_y = self.path[-1]
        
        if direction == "forward":
            new_y = last_y - self.scale # Moving "up" the 2D canvas
            new_x = last_x
        elif direction == "backward":
            new_y = last_y + self.scale # Moving "down" the canvas
            new_x = last_x
        elif direction == "left":
            new_x = last_x - self.scale # Moving "left" on the canvas
            new_y = last_y
        elif direction == "right":
            new_x = last_x + self.scale # Moving "right" on the canvas
            new_y = last_y
        else:
            return # Hover or unknown command, position doesn't change

        # Keep the coordinates within the canvas boundaries
        new_x = max(0, min(self.canvas_size, new_x))
        new_y = max(0, min(self.canvas_size, new_y))
        
        self.path.append((new_x, new_y))

    def save_map(self):
        """
        Draws the lines and saves the final JPEG to the map folder.
        """
        # Create a blank white canvas (1000x1000 pixels, 3 color channels)
        canvas = np.ones((self.canvas_size, self.canvas_size, 3), dtype=np.uint8) * 255
        
        # Draw a faint grid for a technical look
        for i in range(0, self.canvas_size, 50):
            cv2.line(canvas, (i, 0), (i, self.canvas_size), (230, 230, 230), 1)
            cv2.line(canvas, (0, i), (self.canvas_size, i), (230, 230, 230), 1)

        # Draw the flight path line
        for i in range(1, len(self.path)):
            # Draw line from previous point to current point
            cv2.line(canvas, self.path[i-1], self.path[i], (255, 0, 0), 2) # Blue path
            
        # Mark Start Point (Green Circle)
        cv2.circle(canvas, self.path[0], 6, (0, 255, 0), -1)
        cv2.putText(canvas, "START", (self.path[0][0] + 10, self.path[0][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 2)
        
        # Mark End Point (Red Circle)
        cv2.circle(canvas, self.path[-1], 6, (0, 0, 255), -1)
        cv2.putText(canvas, "END", (self.path[-1][0] + 10, self.path[-1][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)

        # Generate filename and save
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.save_dir, f"2D_Flight_Path_{timestamp}.jpg")
        cv2.imwrite(filename, canvas)
        print(f"\n[MAPPER] 2D Flight Path successfully saved to: {filename}")