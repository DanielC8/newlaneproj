img_hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    lowery = np.array([10,95,95], dtype = "uint8")
    uppery = np.array([40,255,255], dtype = "uint8")
    maskt = cv2.inRange(img_hsv,lowery,uppery)
    maskw = cv2.bitwise_and(gray,maskt)
    canny = cv2.Canny(maskw, 30, 200)
    lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, maxLineGap=100, minLineLength=20)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(result, (x1, y1), (x2, y2), (0, 255, 255), 10)

gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
height, width = gray.shape
gauss = cv2.GaussianBlur(gray, (15, 15), 0)

canny = cv2.Canny(gray, 25, 100)
lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 50, maxLineGap=100, minLineLength=20)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if -0.1 < (x1 - x2) / (y1 - y2) < 0.1:
            leftline = (y1 - y2) / (x1 - x2)
            y12 = 0
            x12 = int((y12 - y1) / leftline + x1)
            y22 = int(height)
            x22 = int((y22 - y1) / leftline + x1)
            cv2.line(result, (x12, y12), (x22, y22), (0, 255, 255), 10)