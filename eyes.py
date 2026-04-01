import cv2
import mss
import numpy as np
import time

# Your locked-in scrcpy video feed coordinates
SCRCPY_WINDOW = {"top": 313, "left": 962, "width": 904, "height": 434}

def get_scrcpy_frame(monitor_box=SCRCPY_WINDOW):
    """
    Grabs a specific region of the screen and converts it for OpenCV/YOLO.
    """
    with mss.mss() as sct:
        # Capture the raw screen region
        img = np.array(sct.grab(monitor_box))
        
        # IMPORTANT: mss captures images in BGRA format.
        # YOLO and OpenCV expect BGR. We must convert it.
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        return frame

# ==========================================
# STANDALONE VISION TESTER
# ==========================================
if __name__ == "__main__":
    print("Starting Drone Vision Test...")
    print("Click on the video popup window and press 'q' to quit.")
    
    fps_start_time = time.time()
    fps_counter = 0
    fps = 0 
    
    # --- NEW FIX: Force the window to spawn away from the capture zone ---
    cv2.namedWindow("AI Vision - Live Feed")
    cv2.moveWindow("AI Vision - Live Feed", 0, 0) # Moves it to the top-left of your monitor
    # ---------------------------------------------------------------------
    
    while True:
        # 1. Grab the frame
        frame = get_scrcpy_frame()
        
        # 2. Calculate FPS
        fps_counter += 1
        if (time.time() - fps_start_time) > 1:
            fps = fps_counter
            fps_counter = 0
            fps_start_time = time.time()
            
        # Display FPS on the image
        cv2.putText(frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # 3. Show what the AI sees
        cv2.imshow("AI Vision - Live Feed", frame)
        
        # 4. Emergency Kill Switch for the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()