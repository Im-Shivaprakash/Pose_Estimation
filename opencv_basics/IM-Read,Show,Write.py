import cv2

#Reading an image
img = cv2.imread("opencv_basics\image1.jpeg")

#Writing an image
cv2.imwrite("grayscale.jpg", cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))

#Displaying an image
cv2.imshow("Frame", img)

cv2.waitKey(0)
