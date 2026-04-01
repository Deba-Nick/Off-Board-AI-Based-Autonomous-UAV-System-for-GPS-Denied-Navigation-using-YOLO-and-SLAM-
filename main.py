import cv2
import time
import os
import keyboard
from datetime import datetime
from ultralytics import YOLO
from vision.eyes import get_scrcpy_frame
from control.flight_bridge import (
    ascend, descend, move_forward, move_backward, 
    move_left, move_right, hover
)
# Import the new mapping module
from map.mapper import FlightMapper

# ==========================================
# SYSTEM SETUP
# ==========================================
if not os.path.exists("map"):
    os.makedirs("map")

print("Loading YOLOv8 AI Model...")
model = YOLO("yolov8n.pt")
TARGET_CLASS = 0  

# Global State Variables
manual_target = None
mouse_freed = False
human_intervention = False
evade_attempts = 0

def click_event(event, x, y, flags, param):
    """Listens for manual override clicks when the mouse is freed."""
    global manual_target, mouse_freed, human_intervention, evade_attempts
    if event == cv2.EVENT_LBUTTONDOWN and mouse_freed:
        print(f"\n[MANUAL OVERRIDE] Target Locked at X:{x} Y:{y}")
        manual_target = (x, y)
        mouse_freed = False 
        human_intervention = False # Clear panic state on manual command
        evade_attempts = 0         

def main():
    global manual_target, mouse_freed, human_intervention, evade_attempts
    
    print("\n=========================================")
    print("      DRONE AI PILOT SYSTEM ONLINE       ")
    print("=========================================")
    print("HOTKEYS:")
    print("  [ESC]    : GLOBAL KILL SWITCH. Stops program & saves map.")
    print("  [Ctrl+C] : FREE MOUSE / HUMAN OVERRIDE.")
    print("=========================================\n")
    
    startup = input("Type 'start' and press Enter to begin the mission: ").strip().lower()
    if startup != 'start':
        print("Mission aborted.")
        return

    # Initialize the 2D Path Mapper
    flight_map = FlightMapper(save_dir="map")

    # --- TAKEOFF & ALTITUDE CONTROL ---
    print("\n[FLIGHT] Arming motors...")
    ascend(duration_ms=1000) 
    hover()
    time.sleep(1) 
    
    print("[FLIGHT] Taking off...")
    ascend(duration_ms=2000) 
    hover()
    print("[FLIGHT] Airborne. Maintaining default altitude.")

    alt_choice = input(">>> Do you want to increase altitude before patrolling? (y/n): ").strip().lower()
    if alt_choice == 'y':
        print("[FLIGHT] Pushing altitude up...")
        ascend(duration_ms=1500) 
        hover()
    print("[FLIGHT] Altitude locked. Commencing AI Patrol.\n")

    # ==========================================
    # SETUP VISION WINDOW (Always On Top Fix)
    # ==========================================
    cv2.namedWindow("AI Pilot Brain", cv2.WINDOW_NORMAL)
    cv2.moveWindow("AI Pilot Brain", 0, 0)
    # Force the OpenCV window to float above scrcpy
    cv2.setWindowProperty("AI Pilot Brain", cv2.WND_PROP_TOPMOST, 1)
    cv2.setMouseCallback("AI Pilot Brain", click_event)
    
    map_save_timer = time.time()
    
    while True:
        # --- GLOBAL KILL SWITCH ---
        if keyboard.is_pressed('esc'):
            print("\n[SYSTEM] GLOBAL KILL SWITCH ACTIVATED (ESC).")
            hover() 
            flight_map.save_map() # Save the 2D trajectory before shutting down
            break

        # --- FREE MOUSE TOGGLE ---
        if keyboard.is_pressed('ctrl+c'):
            mouse_freed = not mouse_freed
            if mouse_freed:
                hover()
                human_intervention = False 
                evade_attempts = 0
                print("\n[SYSTEM] Mouse FREED. You have manual control.")
            else:
                print("\n[SYSTEM] Autopilot RE-ENGAGED.")
            time.sleep(0.3) 

        # --- VISION ---
        frame = get_scrcpy_frame()
        height, width, _ = frame.shape
        center_x, center_y = width // 2, height // 2
        frame_area = width * height
        
        # PERIODIC SNAPSHOT ALGORITHM
        if time.time() - map_save_timer > 5.0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f"map/camera_view_{timestamp}.jpg", frame)
            map_save_timer = time.time()

        # ==========================================
        # AI FLIGHT CONTROLLER
        # ==========================================
        if not mouse_freed:
            
            # --- HUMAN INTERVENTION STATE ---
            if human_intervention:
                hover()
                cv2.putText(frame, "CRITICAL: HUMAN INTERVENTION REQUIRED!", (50, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                cv2.putText(frame, "Press Ctrl+C to take manual control.", (50, 150), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 165, 255), 2)
            
            # --- CLICK-TO-GO NAVIGATION ---
            elif manual_target:
                tx, ty = manual_target
                cv2.circle(frame, (tx, ty), 10, (255, 0, 0), -1)
                cv2.putText(frame, "TARGET", (tx - 30, ty - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                deadzone = 80
                moved = False
                
                # Navigate and update 2D map
                if tx < center_x - deadzone: 
                    move_left(duration_ms=200)
                    flight_map.update_position("left")
                    moved = True
                elif tx > center_x + deadzone: 
                    move_right(duration_ms=200)
                    flight_map.update_position("right")
                    moved = True
                    
                if ty < center_y - deadzone: 
                    move_forward(duration_ms=200)
                    flight_map.update_position("forward")
                    moved = True
                elif ty > center_y + deadzone: 
                    move_backward(duration_ms=200)
                    flight_map.update_position("backward")
                    moved = True
                    
                if not moved:
                    hover()
                    manual_target = None
                    print("[FLIGHT] Target reached. Resuming AI patrol.")

            # --- YOLO AUTO-TRACKING & OBSTACLE AVOIDANCE ---
            else:
                results = model.predict(frame, verbose=False)
                
                target_coords = None
                collision_threat = False

                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls_id = int(box.cls[0])
                        label = model.names[cls_id]
                        
                        # Draw boxes around everything
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

                        # Check Collision Threat (> 35% of screen)
                        box_area = (x2 - x1) * (y2 - y1)
                        if (box_area / frame_area) > 0.35:
                            collision_threat = True
                        
                        # Identify tracking target
                        if cls_id == TARGET_CLASS:
                            target_coords = (x1, y1, x2, y2)

                # Flight Logic
                if collision_threat:
                    print("[WARNING] OBSTACLE DETECTED! EVADING!")
                    cv2.putText(frame, "EVADING OBSTACLE!", (width//2 - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                    
                    # Evasive maneuvers & map updates
                    move_backward(duration_ms=600) 
                    flight_map.update_position("backward")
                    
                    move_right(duration_ms=400)    
                    flight_map.update_position("right")
                    
                    evade_attempts += 1
                    
                    if evade_attempts >= 4:
                        print("[CRITICAL] Cannot bypass obstacle. Requesting human intervention.")
                        human_intervention = True

                elif target_coords:
                    evade_attempts = 0 # Reset panic counter
                    x1, y1, x2, y2 = target_coords
                    person_center_x = (x1 + x2) // 2
                    
                    # Highlight target in green
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv2.circle(frame, (person_center_x, (y1+y2)//2), 5, (0, 0, 255), -1)
                    
                    deadzone = 100
                    if person_center_x < (center_x - deadzone): 
                        move_left(duration_ms=200)
                        flight_map.update_position("left")
                    elif person_center_x > (center_x + deadzone): 
                        move_right(duration_ms=200)
                        flight_map.update_position("right")
                    else: 
                        hover()
                
                else:
                    hover() # Chilling, no targets or obstacles
        
        else:
            cv2.putText(frame, "MOUSE FREED - WAITING FOR CLICK", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)

        # Draw central crosshairs
        cv2.line(frame, (center_x - 20, center_y), (center_x + 20, center_y), (0, 255, 255), 2)
        cv2.line(frame, (center_x, center_y - 20), (center_x, center_y + 20), (0, 255, 255), 2)

        cv2.imshow("AI Pilot Brain", frame)
        cv2.waitKey(1) 
            
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()