import cv2

#Reading a video
video = cv2.VideoCapture("opencv_basics\high_knees.mp4")

if not video.isOpened():
    print("Can't be opened")
    exit()

while True:
    ret, frame = video.read()
    if not ret:
        break
    cv2.imshow("Video", frame)
    
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()    