import sys
import cv2
import argparse
from collections import OrderedDict
import numpy as np
import os

parser = argparse.ArgumentParser(description = "")
parser.add_argument("-f", help = "Page image input")
parser.add_argument("-v", help = "Verbose mode", action = 'store_true', default = False)
args = parser.parse_args()

paragraphs = []
lines = []
words = []


def load_coordinates():
    for line in sys.stdin:
        data = line.strip().split()
        # print line.strip()
        data_type = data[0].strip("(")
        try:
            coordinates = tuple([int(x) for x in data[1:5]])
            # print coordinates
            # print line.strip()
        except ValueError:
            continue
        print data_type, coordinates
        if data_type == "para":
            paragraphs.append(coordinates)
        elif data_type == "line":
            lines.append(coordinates)
        elif data_type == "word":
            words.append(coordinates)
        else:
            continue


def remove_words(image):
    for coord in words:
        x1, y1, x2, y2 = coord
        cv2.rectangle(image, (x1, y1), (x2, y2), 0, thickness= -1) 


def preprocess_image(original):
    image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    
    ## Thresholding
    otsu_value, thresholded = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    ## Cover words
    remove_words(thresholded) 
   
    ## Thicken skeleton
    thickened = cv2.dilate(thresholded, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)), iterations = 1)

    return thickened


def find_rectangles(original, thickened):
    rectangles = []
    (contours, _) = cv2.findContours(thickened.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

    rect_image = original.copy()

    for i, cnt in enumerate(contours):
        x, y, w, h = cv2.boundingRect(cnt)
        x1, y1, x2, y2 = x, y, x + w, y + h
        roi = original[y1:y2 + 1, x1:x2 + 1]
        height, width, channels = roi.shape
        if height > 10 and width > 10:
            rectangles.append((x, y, x + w, y + h))

    if args.v:
        rect_output = args.f.strip(".full.tiff") + ".rect.tiff"
        skel_output = args.f.strip(".full.tiff") + ".skel.tiff"
        rect_dir = args.f.strip(".full.tiff")
        os.mkdir(rect_dir)
        
        enum = 0
        for x1, y1, x2, y2 in rectangles:
            height = y2 - y1
            width = x2 - x1
            if height > 30 and width > 30:
                cv2.imwrite(rect_dir + "/rect_" + str(enum) + ".tiff", original[y1:y2 + 1, x1:x2 + 1])
                enum += 1
            cv2.rectangle(rect_image, (x1, y1), (x2, y2), (255,0,0) ,5)

        cv2.imwrite(rect_output, rect_image)
        cv2.imwrite(skel_output, thickened)
   
    for x1, y1, x2, y2 in rectangles:
       rectangle = {"X1":str(x1), "Y1":str(y1), "X2":str(x2), "Y2":str(y2)}
       for param in ["X1", "Y1", "X2", "Y2"]:
           sys.stdout.write(param + ":" + str(rectangle[param]) + "\t")
       sys.stdout.write("\n")



if __name__ == "__main__":

    for line in sys.stdin:
        words.append(tuple([int(x) for x in line.strip().split()]))

    # load_coordinates()
    original = cv2.imread(args.f)
    thickened = preprocess_image(original)
    find_rectangles(original, thickened)
