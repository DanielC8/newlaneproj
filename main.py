import cv2
import numpy as np
video = cv2.VideoCapture("Lane2.mp4")
leftl = []
rightl = []
count = 0
left_cascade = cv2.CascadeClassifier('left.xml')

while True:
   ret, frame = video.read()
   if not ret:
       break
   frame = cv2.imread("left.png")
   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   height, width = gray.shape



   canny = cv2.Canny(gray, 100, 200)
   faces = left_cascade.detectMultiScale(gray, 1.3, 3)
   for (x, y, w, h) in faces:
       cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=3)
       cv2.rectangle(canny, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 0), thickness=-1)
   lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, maxLineGap=20, minLineLength=400)

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
