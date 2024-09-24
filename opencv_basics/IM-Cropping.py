import cv2

img = cv2.imread('opencv_basics\Astro.png')

print(img.shape)

cropped_img = img[400:900, 400:1200]

cv2.imshow("Image", img)

cv2.imshow("Frame", cropped_img)

cv2.waitKey(0)