def calculate_evasion(x1, x2, frame_width):
    # Calculate the center of the obstacle and its width
    x_center = (x1 + x2) / 2
    box_width = x2 - x1

    # Proximity Check: If it takes up less than 30% of the screen, ignore it
    if box_width < (frame_width * 0.3):
        return None 

    # Zone Logic: Divide screen into thirds
    left_boundary = frame_width / 3
    right_boundary = (frame_width * 2) / 3

    if x_center < left_boundary:
        return "[EVASION] Obstacle LEFT -> Command: ROLL RIGHT"
    elif x_center > right_boundary:
        return "[EVASION] Obstacle RIGHT -> Command: ROLL LEFT"
    else:
        return "[EVASION] Obstacle CENTER -> Command: PITCH BACK (REVERSE)"