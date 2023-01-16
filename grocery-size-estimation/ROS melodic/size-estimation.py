#!/usr/bin/env python
import rospy
from std_msgs.msg import String

# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2

def take_picture():
    cam = cv2.VideoCapture(2) # camport = 2 for juno
    result, image = cam.read()
    
    # If image will detected without any error,
    # show result
    if result:
        return image

    # If captured image is corrupted, moving to else part
    else:
        print("No image detected. Please! try again")

def image_preprocessing(image):
    
    # Convert image to grayscale and blur slighly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # Perform edge detection, dilation, erotion
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=5) 
    edged = cv2.erode(edged, None, iterations=1)

    
    return edged

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
    
def get_size(ori_img, prep_img,width):
    # Find contours in the edge map
    cnts = cv2.findContours(prep_img.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    (cnts, _) = contours.sort_contours(cnts) # sort the contours from left-to-right

    pixelsPerMetric = None # 'pixels per metric' calibration variable

    # loop over the contours individually
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 1000: # edit this according to dataset
            continue

        # compute the rotated bounding box of the contour
        orig = ori_img.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
        
        # list to store width
        item_width = []

        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        # unpack the ordered bounding box, then compute the midpoint
            # between the top-left and top-right coordinates, followed by
            # the midpoint between bottom-left and bottom-right coordinates
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
        
        # compute the midpoint between the top-left and bottom-left points,
            # followed by the midpoint between the top-righ and bottom-right
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)

        # draw the midpoints on the image
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
        
        # draw lines between the midpoints
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                (255, 0, 255), 2)

        # compute the Euclidean distance between the midpoints
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # Initialize if pPM is none
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / width

    # compute the size of the object
        dimA = round((dA / pixelsPerMetric),1)
        dimB = round((dB / pixelsPerMetric),1)
        
        item_width.append(dimB)

        print("Height:" , dimA)
        print("Width:" , dimB)  

    # draw the object sizes on the image
        cv2.putText(orig, "H: {:.1f}cm".format(dimA),
            (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)
        cv2.putText(orig, "W: {:.1f}cm".format(dimB),
            (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)

        cv2.imshow("Image",orig)
        cv2.waitKey(1000)
   
    return item_width[0]

def append_to_file(file_name, text_to_append):
    # Open the file in append mode
    with open(file_name, "r") as file_object:
    # Read the contents of the file into a list of lines
        lines = file_object.readlines()

    # Modify the last line of the file
    lines[-1] = lines[-1] + ":" + str(text_to_append)

    # Open the file in write mode
    with open(file_name, "w") as file_object:
        # Write the modified lines back to the file
        file_object.writelines(lines)

def main():
    
    # Take picture using juno camera
    ori_img = take_picture()

    # width of reference obj
    width = 5.0

    # Pre-process Image 
    prep_img = image_preprocessing(ori_img)

    # Perform size estimation
    output = get_size(ori_img, prep_img, width) 
    
    # Get width and append to file
    grocerylist = '/home/mustar/catkin_ws/src/mad_fyp/src/size.txt'
    append_to_file(grocerylist,output)

if __name__=="__main__":
    main()

