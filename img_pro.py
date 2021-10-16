import cv2
import numpy as np
import math
import time
import csv


def log_params(degree=None, cx=None, cy=None, contourArea=None):
    #logging params into a csv file
    header = ["Coordinates", "Degree", "Cam Position", "Contour Area"]
    with open("logs.csv", "a", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)
        #writing the header
        writer.writerow(header)

        #writing the data
        writer.writerow([degree, (cx, cy), contourArea])


def log_coords(vehicle_coordinates):
    header = ["Coordinates"]
    with open("coords.csv", "a", encoding="UTF-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow([vehicle_coordinates])

def calcDegree(camx, camy, cx, cy):
    #calculating the degree between center of object and center of cam
    try:
        #finding slope by using analitic geometry
        slope = (camy- cy) / (cx- camx)
        #using math library for calculating radian value and transforming to degree of that slope
        radian = math.atan(slope)
        degree = math.degrees(radian)
        print("degree", degree)
        return degree
    except ZeroDivisionError:
        #at some point zerodivisonerror may occur.
        return 0


def detect_circle(waittime=5, Vehicle_coordinates=None):
    #detecting a circle with a spesific color
    #waittime is for countdown
    ptime = time.time() # getting time info for countdown

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    #hsv ranges of blue color
    blue_lower=np.array([0,116,111],np.uint8)
    blue_upper=np.array([141,255,255],np.uint8)

    #getting width and height specs of cam in order to calculate degrees
    camx = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
    camy = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2)

    while True: 
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) #for masking operations
        if ret:
            mask = cv2.inRange(hsv, blue_lower, blue_upper)
            kernel = np.ones((7,7),np.uint8) # a kernel to apply noise reductions

            # Remove unnecessary noise from mask
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            #finding contours
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                #these lines of codes are for detecting whether if objects shape is circle or not
                approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
                area = cv2.contourArea(contour)
                #also we add area > 2000 to eliminate unnecessery results
                if len(approx)  > 8 and area > 2000:
                    
                    #using moments to calc center of shape
                    M = cv2.moments(contour)
                    cx = int(M["m10"]/M["m00"])
                    cy = int(M["m01"]/M["m00"])

                    degree = calcDegree(camx, camy, cx, cy)
                    print("Degree between camera and object is {}".format(degree))
                    try:
                        log_params(degree, cx, cy, area)
                    except:
                        continue
                    #for visual log
                    cv2.line(frame, (camx, camy), (cx, cy), (0, 0, 255), 4)
                    cv2.putText(frame, "X: {} - Y: {}".format(cx, cy), (15, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    frame = cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)

            cv2.imshow("output", frame)
            if cv2.waitKey(5) and time.time() - ptime > waittime:
                cap.release()
                cv2.destroyAllWindows()
                break
