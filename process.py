import cv2
import numpy as np


def process(frame,leftl,rightl,count):
    #Gets cascades and images
    car_cascade = cv2.CascadeClassifier('car2.xml')
    warning = cv2.imread("warning.png")
    forward = cv2.imread("forward.png")

    #turns to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #Apply Gaussian Blur
    gauss = cv2.GaussianBlur(gray, (15, 15), 0)
    #Apply Canny Edge
    canny = cv2.Canny(gauss, 5, 30)
    #Apply mask
    height, width = gray.shape
    area = np.array([[(int(width / 2), int(height / 2)+50), (width, height), (0, height)]])
    mask = np.zeros_like(gray)
    mask = cv2.fillPoly(mask, area, 255)
    maskcanny = cv2.bitwise_and(canny, mask)
    #Apply car detection
    car = car_cascade.detectMultiScale(gray, 1.3, 2)
    for (x, y, w, h) in car:
        if h*w / (height*width) >= 0.20:
            #Applies warning if car is large portion of screen
            frame[125:250,250:375,:] = warning[0:125,0:125,:]
            print("warning")
        #blacks out car
        cv2.rectangle(maskcanny, pt1=(x, y), pt2=(x + w, y + h), color=(0, 0, 0), thickness=-1)
    #apply hough lines
    lines = cv2.HoughLinesP(maskcanny, 1, np.pi / 180, 50, maxLineGap=100, minLineLength=80)
    leftslope = []
    rightslope = []
    slopedict  = {}
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            y1 = height - y1
            y2 = height - y2
            #gets slopes
            if x1 == x2:
                slope = 999999999
                break
            else:
                slope = (y1-y2)/(x1-x2)
            slopedict[(x1,y1,x2,y2)] = slope
            #appends slopes to corresponding list
            if slope > 0:
                leftslope.append(slope)
            elif -0.5 <= slope <= 0.5:
                pass
            else:
                rightslope.append(slope)
    if leftslope != []:
        #get maximum slope and output line
        count = 0
        leftline = max(leftslope)
        points = []
        for pointset in slopedict:
            if slopedict[pointset] == leftline:
                points.append(pointset)

        np.array(points)
        np.average(points)
        y1 = 0
        x1 = int((y1 - points[0][1])/leftline + points[0][0])
        y2 = int(height/2)-50
        x2 = int((y2 - points[0][1])/leftline + points[0][0])
        leftl = [x1, y1, x2, y2]

        cv2.line(frame, (x1, height - y1), (x2, height - y2), (0, 255, 255), 10)
    elif leftl != [] and count < 10:
        #output previous line if count is less than 10
        count += 1
        cv2.line(frame, (leftl[0], height - leftl[1]), (leftl[2], height - leftl[3]), (0, 255, 0), 10)

    if rightslope != []:
        #get minimum slope for right line and output it
        count = 0
        rightline = min(rightslope)
        points = []
        for pointset in slopedict:
            if slopedict[pointset] == rightline:
                points.append(pointset)
        np.array(points)
        np.average(points)
        y1 = 0
        x1 = int((y1 - points[0][1]) / rightline + points[0][0])
        y2 = int(height / 2)-50
        x2 = int((y2 - points[0][1]) / rightline + points[0][0])
        rightl = [x1,y1,x2,y2]
        cv2.line(frame, (x1, height - y1), (x2, height - y2), (0, 255, 0), 10)
    elif rightl != [] and count <10:
        #output previous line if count is less than 10
        count +=1
        cv2.line(frame, (rightl[0], height - rightl[1]), (rightl[2], height - rightl[3]), (0, 255, 0), 10)

    if rightl != [] and leftl != [] and count <10:
        #Gets midline
        cv2.line(frame, (int((rightl[0]+leftl[0])/2), height - rightl[1]), (int((rightl[2]+leftl[2])/2), height - rightl[3]), (0, 255, 0), 10)
    #outputs direction of travel
    frame[125:125+93, 600:600+93, :] = forward[0:93, 0:93, :]
    return([frame,leftl,rightl,count])




