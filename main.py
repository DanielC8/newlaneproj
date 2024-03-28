import cv2
import numpy as np
video = cv2.VideoCapture("Lane2.mp4")
leftl = []
rightl = []
count = 0

while True:
   ret, frame = video.read()
   if not ret:
       break
   frame = cv2.imread("left.png")
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   height, width = gray.shape



   canny = cv2.Canny(gray, 100, 200)
   lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, maxLineGap=20, minLineLength=10)

   intercepts = {}
   if lines is not None:
       for line in lines:
           x1, y1, x2, y2 = line[0]

           cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 10)



   cv2.imshow("Output", frame)
   cv2.imshow("ee", canny)






   if cv2.waitKey(0) & 0xFF == ord('q'):
       break

video.release()
cv2.destroyAllWindows()
