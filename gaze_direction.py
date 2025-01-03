from gaze_tracking import GazeTracking
import cv2

# Initialize GazeTracking
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)  # Open the default camera

print("Press 'q' to quit.")

while True:
    # Capture a frame from the webcam
    _, frame = webcam.read()

    # Analyze the frame for gaze tracking
    gaze.refresh(frame)

    # Get the annotated frame (optional for visualization)
    frame = gaze.annotated_frame()

    # Determine the direction of the gaze
    if gaze.is_blinking():
        text = "Blinking"
    elif gaze.is_right():
        text = "Looking right"
    elif gaze.is_left():
        text = "Looking left"
    elif gaze.is_center():
        text = "Looking center"
    else:
        text = "No gaze detected"

    # Display the result on the frame
    cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the video feed with annotations
    cv2.imshow("Gaze Tracking", frame)

    # Print the gaze direction in the terminal
    print(text)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
webcam.release()
cv2.destroyAllWindows()

