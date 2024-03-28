import cv2
import numpy as np
video = cv2.VideoCapture("Lane2.mp4")
leftl = []
rightl = []
count = 0
car_cascade = cv2.CascadeClassifier('cars.xml')

while True:
   ret, frame = video.read()
   if not ret:
       break

   gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
   height, width = gray.shape

   pts1 = np.float32([[int(width/2)-100, 415], [int(width/2)+100, 415],[0, height], [width, height]])


   pts2 = np.float32([[int((int(width/2)-100)/2), 0], [(int((width/2)+100+width)/2), 0],[int((int(width/2)-100)/2), height], [(int((width/2)+100+width)/2), height]])

   matrix = cv2.getPerspectiveTransform(pts1, pts2)
   result = cv2.warpPerspective(frame, matrix, (width, height))

   gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)


   canny = cv2.Canny(gray, 30, 200)
   lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, maxLineGap=20, minLineLength=10)

   intercepts = {}
   if lines is not None:
       for line in lines:
           x1, y1, x2, y2 = line[0]

           cv2.line(result, (x1, y1), (x2, y2), (0, 255, 255), 10)



   cv2.imshow("Output", frame)
   cv2.imshow("ee", canny)

   cv2.imshow("eeee", result)




   if cv2.waitKey(0) & 0xFF == ord('q'):
       break

video.release()
cv2.destroyAllWindows()
