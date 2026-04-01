import pyautogui
import time

print("--- BOUNDING BOX FINDER ---")
print("1. Move your mouse to the TOP-LEFT corner of the scrcpy video feed.")
print("   (Wait 3 seconds...)")
time.sleep(3)
left, top = pyautogui.position()
print(f"Top-Left locked at: X {left}, Y {top}")

print("\n2. Now move your mouse to the BOTTOM-RIGHT corner of the scrcpy video feed.")
print("   (Wait 3 seconds...)")
time.sleep(3)
right, bottom = pyautogui.position()
print(f"Bottom-Right locked at: X {right}, Y {bottom}")

# Calculate width and height
width = right - left
height = bottom - top

print("\n=== YOUR MSS BOUNDING BOX ===")
print(f'{{"top": {top}, "left": {left}, "width": {width}, "height": {height}}}')
print("=============================")