from gaze_tracking import GazeTracking
import cv2

# Initialize GazeTracking
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

if not webcam.isOpened():
    print("Error: Unable to access the camera.")
    exit()

# Instructions for the user
print("Look at each point (A, B, C, D, E) and press 's' to save the horizontal ratio.")
print("Press 'q' to quit.")

# Data storage
ratios = []

while True:
    # Capture frame from the webcam
    _, frame = webcam.read()
    if frame is None:
        print("Error: Unable to capture frame.")
        break

    # Analyze the frame
    gaze.refresh(frame)

    # Get the horizontal ratio
    if gaze.pupils_located:
        horizontal_ratio = gaze.horizontal_ratio()
        display_text = f"Horizontal Ratio: {horizontal_ratio:.2f}"
    else:
        display_text = "Pupils not located"

    # Get the frame dimensions
    frame_height, frame_width, _ = frame.shape

    # Text settings
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2  # Large text
    font_thickness = 3
    text_color = (0, 255, 0) if gaze.pupils_located else (0, 0, 255)

    # Calculate text size and position
    text_size = cv2.getTextSize(display_text, font, font_scale, font_thickness)[0]
    text_x = (frame_width - text_size[0]) // 2  # Center horizontally
    text_y = (frame_height + text_size[1]) // 2  # Center vertically

    # Add text to the frame
    cv2.putText(frame, display_text, (text_x, text_y), font, font_scale, text_color, font_thickness)

    # Show the video feed
    cv2.imshow("Gaze Tracking", frame)

    # Save data on 's' key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and gaze.pupils_located:
        print("\nRatio saved!")
        ratios.append(horizontal_ratio)

    # Quit on 'q' key press
    if key == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

# Save ratios to a file or print them
print("\nSaved Ratios:", ratios)
with open("horizontal_ratios.txt", "w") as f:
    for ratio in ratios:
        f.write(f"{ratio}\n")

print("Ratios saved to 'horizontal_ratios.txt'")
