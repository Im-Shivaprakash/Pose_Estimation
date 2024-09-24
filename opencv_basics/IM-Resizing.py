import cv2

img = cv2.imread("opencv_basics\image2.jpeg")

scale_down_img = cv2.resize(img, (200, 200), interpolation = cv2.INTER_LINEAR)

scale_up_img = cv2.resize(img, (800, 800), interpolation=cv2.INTER_LINEAR)

cv2.imshow("Scale Down", scale_down_img)
cv2.waitKey(0)

cv2.imshow("Scale Up", scale_up_img)
cv2.waitKey(0)
