# Corrected thresholds for horizontal ratio
LEFT_MIN = 0.6825
LEFT_MAX = 0.8930
CENTER_MIN = 0.4300
CENTER_MAX = 0.7195
RIGHT_MIN = 0.2653
RIGHT_MAX = 0.4400

# Variables to track consecutive frames
current_gaze = None
consecutive_count = 0
stable_gaze = None
FRAMES_REQUIRED = 3  # Number of frames to hold gaze

def classify_gaze(horizontal_ratio):
    """
    Classifies gaze direction based on horizontal ratio thresholds.
    :param horizontal_ratio: Float value of the horizontal ratio
    :return: String indicating gaze direction ('Left', 'Center', 'Right', or 'Unknown')
    """
    if LEFT_MIN <= horizontal_ratio <= LEFT_MAX:
        return "Left"
    elif CENTER_MIN <= horizontal_ratio <= CENTER_MAX:
        return "Center"
    elif RIGHT_MIN <= horizontal_ratio <= RIGHT_MAX:
        return "Right"
    else:
        return "Unknown"

# Example Usage with OpenCV for live testing
import cv2
from gaze_tracking import GazeTracking

gaze = GazeTracking()
webcam = cv2.VideoCapture(1)

if not webcam.isOpened():
    print("Error: Unable to access the camera.")
    exit()

print("Press 'q' to quit.")

while True:
    # Capture frame from the webcam
    _, frame = webcam.read()
    if frame is None:
        print("Error: Unable to capture frame.")
        break

    # Analyze the frame
    gaze.refresh(frame)

    # Determine the horizontal ratio and gaze direction
    if gaze.pupils_located:
        horizontal_ratio = gaze.horizontal_ratio()
        detected_gaze = classify_gaze(horizontal_ratio)

        # Check if the detected gaze is the same as the previous frame
        if detected_gaze == current_gaze:
            consecutive_count += 1
        else:
            consecutive_count = 1
            current_gaze = detected_gaze

        # Update the stable gaze if held for the required number of frames
        if consecutive_count >= FRAMES_REQUIRED:
            stable_gaze = detected_gaze

        # Print the current horizontal ratio and detected gaze
        print(f"Horizontal Ratio: {horizontal_ratio:.4f} | Detected Gaze: {detected_gaze}")
    else:
        stable_gaze = "Pupils not located"
        consecutive_count = 0
        print("Horizontal Ratio: None | Pupils not located")

    # Display the stable gaze direction
    display_text = stable_gaze if stable_gaze else "Detecting..."
    frame_height, frame_width, _ = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 3
    text_color = (0, 255, 0) if stable_gaze != "Pupils not located" else (0, 0, 255)
    text_size = cv2.getTextSize(display_text, font, font_scale, font_thickness)[0]
    text_x = (frame_width - text_size[0]) // 2
    text_y = (frame_height + text_size[1]) // 2

    cv2.putText(frame, display_text, (text_x, text_y), font, font_scale, text_color, font_thickness)

    # Show the video feed
    cv2.imshow("Gaze Tracking", frame)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()