import cv2
import numpy as np
video = cv2.VideoCapture("Lane2.mp4")
leftl = []
rightl = []
count = 0
car_cascade = cv2.CascadeClassifier('car2.xml')

while True:
    ret, frame = video.read()
    if not ret:
        break

    dup = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gauss = cv2.GaussianBlur(gray, (15, 15), 0)
    canny = cv2.Canny(gauss, 5, 30)

    height, width = gray.shape
    area = np.array([[(int(width / 2), int(height / 2)-100), (width, height), (0, height)]])
    mask = np.zeros_like(gray)
    mask = cv2.fillPoly(mask, area, 255)
    gray = cv2.bitwise_and(gray, mask)
    faces = car_cascade.detectMultiScale(gray, 1.3, 3)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=(255, 0, 0), thickness=3)
        cv2.rectangle(canny, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 0), thickness=-1)


    cv2.imshow("Output", frame)
    cv2.imshow("Input", dup)
    cv2.imshow("e", canny)


    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()