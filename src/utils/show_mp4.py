
import cv2

video_file = "screen_monitor_1.mp4"

cap = cv2.VideoCapture(video_file)

if not cap.isOpened():
    print("Error: cannot open video file")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Video Player", frame)

    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
