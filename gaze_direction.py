import cv2
import serial
import time
from gaze_tracking import GazeTracking

# Serial communication setup for Flipper Zero
SERIAL_PORT = '/dev/cu.usbmodemflip_Ouyidot1'  # Replace with your serial port. can be found by `ls /dev/*usbmodem*`
BAUD_RATE = 115200

# Commands for each gaze direction, this is based on my IR remote & KVM receiver. I had to read it from my flipper first
COMMANDS = {
    "Left": "ir tx NEC 0x17 0x44\r\n",   # Left command
    "Center": "ir tx NEC 0x17 0x43\r\n",  # Center command
    "Right": "ir tx NEC 0x17 0x07\r\n"    # Right command
}

# Thresholds for gaze direction, this is based on my desk setup. is "optimal" for my monitor set up. had to do a lot of tests to find the correct threshold
LEFT_MIN = 0.6825
LEFT_MAX = 0.8930
CENTER_MIN = 0.4268
CENTER_MAX = 0.7195
RIGHT_MIN = 0.2653
RIGHT_MAX = 0.4653


#Classifies gaze direction based on horizontal ratio thresholds.
def classify_gaze(horizontal_ratio):
    if LEFT_MIN <= horizontal_ratio <= LEFT_MAX:
        return "Left"
    elif CENTER_MIN <= horizontal_ratio <= CENTER_MAX:
        return "Center"
    elif RIGHT_MIN <= horizontal_ratio <= RIGHT_MAX:
        return "Right"
    else:
        return "Unknown"

# Initialize gaze tracking
gaze = GazeTracking()

# Initialize serial communication
try:
    flipper = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to Flipper Zero on {SERIAL_PORT}")
except Exception as e:
    print(f"Error connecting to Flipper Zero: {e}")
    exit()

# Start webcam feed
webcam = cv2.VideoCapture(1) #had to choose 1 for me because it kept defaulting to my iPhone
if not webcam.isOpened():
    print("Error: Unable to access the camera.")
    exit()
print("Press 'q' to quit.")

stable_gaze = None
consecutive_count = 0
FRAMES_REQUIRED = 6  # Number of frames required to confirm a gaze

while True:
    _, frame = webcam.read()
    if frame is None:
        print("Error: Unable to capture frame.")
        break

    # Analyze the frame
    gaze.refresh(frame)

    # Determine the gaze direction
    if gaze.pupils_located:
        horizontal_ratio = gaze.horizontal_ratio()
        detected_gaze = classify_gaze(horizontal_ratio)

        # Track stable gaze for consecutive frames
        if detected_gaze == stable_gaze:
            consecutive_count += 1
        else:
            consecutive_count = 1
            stable_gaze = detected_gaze

        # Send IR command if gaze direction is stable
        if consecutive_count >= FRAMES_REQUIRED and stable_gaze in COMMANDS:
            command = COMMANDS[stable_gaze]
            flipper.write(command.encode('utf-8'))
            print(f"Gaze: {stable_gaze} | Sent Command: {command.strip()}")

        print(f"Horizontal Ratio: {horizontal_ratio:.4f} | Detected Gaze: {detected_gaze}")
    else:
        print("Pupils not located.")
        stable_gaze = None
        consecutive_count = 0

    # Display the video feed
    display_text = stable_gaze if stable_gaze else "Detecting..."
    frame_height, frame_width, _ = frame.shape
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 3
    text_color = (0, 255, 0) if stable_gaze else (0, 0, 255)
    text_size = cv2.getTextSize(display_text, font, font_scale, font_thickness)[0]
    text_x = (frame_width - text_size[0]) // 2
    text_y = (frame_height + text_size[1]) // 2

    cv2.putText(frame, display_text, (text_x, text_y), font, font_scale, text_color, font_thickness)
    cv2.imshow("Gaze Tracking", frame)

    # Quit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
webcam.release()
cv2.destroyAllWindows()
flipper.close()
print("Disconnected from Flipper Zero.")