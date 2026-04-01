import pyautogui
import time

print("Press Ctrl+C in this terminal to stop the script.\n")
print("Move your mouse over the scrcpy window to find the new coordinates...")

try:
    while True:
        # Get the current mouse X and Y on your PC monitor
        x, y = pyautogui.position()
        
        # Print it out nicely (the \r keeps it on one line)
        print(f"Monitor Coordinates -> X: {x:4d}, Y: {y:4d}", end="\r")
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("\n\nCoordinate mapping complete!")