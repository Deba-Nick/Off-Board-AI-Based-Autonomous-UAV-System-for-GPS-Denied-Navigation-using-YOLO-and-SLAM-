import pyautogui
import time

# ==========================================
# SAFETY FIRST: THE KILL SWITCH
# ==========================================
# If the drone does something unexpected, slam your physical laptop mouse 
# cursor into ANY of the 4 corners of your screen. This will trigger the failsafe
# and instantly crash the Python script, stopping all commands.
pyautogui.FAILSAFE = True

def drag_joystick(start_x, start_y, end_x, end_y, hold_time_ms=500):
    """
    Moves the mouse to the center of the joystick, clicks down, 
    drags to the target coordinate, holds it, and releases.
    """
    # Convert ms to seconds for the sleep function
    hold_time_sec = hold_time_ms / 1000.0
    
    # 1. Move to the center of the joystick
    pyautogui.moveTo(start_x, start_y)
    
    # 2. Click and hold down the left mouse button
    pyautogui.mouseDown()
    
    # 3. Drag the mouse to the new coordinate (takes 0.2 seconds for a smooth swipe)
    pyautogui.moveTo(end_x, end_y, duration=0.2)
    
    # 4. Hold the joystick in that position to keep the drone moving
    time.sleep(hold_time_sec)
    
    # 5. Let go of the mouse button (the digital joystick should snap back to center)
    pyautogui.mouseUp()

# ==========================================
# LEFT JOYSTICK CONTROLS (Ascend/Descend)
# Center: X 1186, Y 552
# ==========================================

def ascend(duration_ms=500):
    print("Command: Ascend")
    drag_joystick(1186, 552, 1181, 475, duration_ms)

def descend(duration_ms=500):
    print("Command: Descend")
    drag_joystick(1186, 552, 1185, 637, duration_ms)

# ==========================================
# RIGHT JOYSTICK CONTROLS (Forward/Backward/Sideways)
# Center: X 1639, Y 562
# ==========================================

def move_forward(duration_ms=500):
    print("Command: Forward")
    drag_joystick(1639, 562, 1636, 475, duration_ms)

def move_backward(duration_ms=500):
    print("Command: Backward")
    drag_joystick(1639, 562, 1640, 637, duration_ms)

def move_left(duration_ms=500):
    print("Command: Move Left")
    drag_joystick(1639, 562, 1557, 556, duration_ms)

def move_right(duration_ms=500):
    print("Command: Move Right")
    drag_joystick(1639, 562, 1729, 554, duration_ms)

# ==========================================
# HOVER / STOP
# ==========================================

def hover():
    """
    Releases the mouse button just in case it got stuck, 
    allowing both joysticks to snap back to center.
    """
    print("Command: Hover (Releasing Mouse)")
    pyautogui.mouseUp()