import time
from control.flight_bridge import (
    ascend, descend, move_forward, move_backward, 
    move_left, move_right, hover
)

def main():
    print("=========================================")
    print("      DRONE ADB CONTROL TESTER           ")
    print("=========================================")
    print("Ensure your phone is plugged in, unlocked,")
    print("and the drone app is open on the screen.")
    print("NOTE: KEEP THE PHYSICAL DRONE TURNED OFF.\n")

    while True:
        print("\n--- Command Menu ---")
        print("[w] Forward    [s] Backward")
        print("[a] Move Left  [d] Move Right")
        print("[i] Ascend     [k] Descend")
        print("[h] Hover (Reset Joysticks)")
        print("[q] Quit Tester")
        
        choice = input("\nEnter a command letter: ").lower().strip()
        
        if choice == 'w':
            move_forward()
        elif choice == 's':
            move_backward()
        elif choice == 'a':
            move_left()
        elif choice == 'd':
            move_right()
        elif choice == 'i':
            ascend()
        elif choice == 'k':
            descend()
        elif choice == 'h':
            hover()
        elif choice == 'q':
            print("Exiting tester. Safe flights!")
            break
        else:
            print("Invalid command. Try again.")
            
        # Add a tiny delay to let ADB breathe between rapid inputs
        time.sleep(0.5)

if __name__ == "__main__":
    main()