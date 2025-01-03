import time
from gaze_tracking import GazeTracking
import cv2

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

frame_count = 0
start_time = time.time()

while True:
    _, frame = webcam.read()
    if frame is None:
        break

    # Analyze the frame
    gaze.refresh(frame)

    # Count the frame
    frame_count += 1

    # Display the video feed
    cv2.imshow("Gaze Tracking", gaze.annotated_frame())

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print detections per second every second
    if elapsed_time >= 1:
        print(f"Detections per second: {frame_count}")
        frame_count = 0
        start_time = time.time()

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()
