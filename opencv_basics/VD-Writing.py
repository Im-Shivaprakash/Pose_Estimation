import cv2

cap = cv2.VideoCapture(0)

vid_width = int(cap.get(3))
vid_height = int(cap.get(4))

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, frameSize=(vid_width, vid_height))

if not cap.isOpened():
    print("Cam is not available")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    out.write(frame)
    
    cv2.imshow("LIVE", frame)
    
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
    
    
        