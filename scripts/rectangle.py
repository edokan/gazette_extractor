import sys
import cv2
import argparse
from collections import OrderedDict
import numpy as np
import os

parser = argparse.ArgumentParser(description = 
        """
        Generates potential necrology rectangles.
        """
        )
parser.add_argument("-f", help = "Page image input", required = True)
parser.add_argument("-l", help = "Lower bound of possible rectangle", type = int, required = True)
parser.add_argument("-u", help = "Upper bound of possible rectangle", type = int, required = True)
parser.add_argument("-v", help = "Verbose mode", action = 'store_true', default = False)
args = parser.parse_args()

paragraphs = []
lines = []
words = []


def load_coordinates():
    """
    Load word coordinates from preprocessed xml file.
    """

    for line in sys.stdin:
        data = line.strip().split()
        data_type = data[0]
        try:
            coordinates = tuple([int(x) for x in data[1:5]])
        except ValueError:
            continue
        if data_type == "PARAGRAPH":
            paragraphs.append(coordinates)
        elif data_type == "LINE":
            lines.append(coordinates)
        elif data_type == "WORD":
            words.append(coordinates)
        else:
            continue


def remove_words(image):
    """
    Cover words on image with filled rectanges.
    """

    for coord in words:
        x1, y1, x2, y2 = coord
        cv2.rectangle(image, (x1, y1), (x2, y2), 0, thickness= -1) 


def preprocess_image(original):
    """
    Preprocess page image to find rectangles.
    """

    image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    
    ## Thresholding
    otsu_value, thresholded = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    ## Cover words
    remove_words(thresholded) 
   
    ## Thicken skeleton
    thickened = cv2.dilate(thresholded, cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)), iterations = 1)

    return thickened


def find_rectangles(original, thickened):
    """
    Find potential necrology coordinates and print them.
    """

    rectangles = []
    contours, hierarchy = cv2.findContours(thickened.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

    rect_image = original.copy()
    # unimportant_rect = set()

    for i, cnt in enumerate(contours):
        # if hierarchy[0, i, 3] == -1:
        x, y, w, h = cv2.boundingRect(cnt)
        x1, y1, x2, y2 = x, y, x + w, y + h
        roi = original[y1:y2 + 1, x1:x2 + 1]
        height, width, channels = roi.shape
        if (height > args.l and width > args.l) and (height < args.u and width < args.u):
            # if hierarchy[0, i, 3] == -1 or (i in unimportant_rect):
            rectangles.append((x, y, x + w, y + h))
        # else:
            # unimportant_rect.add(i)

    if args.v:
        rect_output = args.f.replace(".tiff", ".rect.tiff")
        skel_output = args.f.replace(".tiff", "skel.tiff")
        rect_dir = args.f.replace(".tiff", "")
        if not os.path.exists(rect_dir):
            os.makedirs(rect_dir)

        enum = 0
        for x1, y1, x2, y2 in rectangles:
            height = y2 - y1
            width = x2 - x1
            filename = rect_dir + "/" + str(x1) + "_" + str(y1) + "_" + str(x2) + "_" + str(y2) + ".tiff"
            cv2.imwrite(filename, original[y1:y2 + 1, x1:x2 + 1])
            enum += 1
            cv2.rectangle(rect_image, (x1, y1), (x2, y2), (255,0,0) ,5)

        cv2.imwrite(rect_output, rect_image)
        cv2.imwrite(skel_output, thickened)
   
    for x1, y1, x2, y2 in rectangles:
       rectangle = {"X1":str(x1), "Y1":str(y1), "X2":str(x2), "Y2":str(y2)}
       for param in ["X1", "Y1", "X2", "Y2"]:
           sys.stdout.write(param + ":" + str(rectangle[param]) + " ")
       sys.stdout.write("\n")


if __name__ == "__main__":
    load_coordinates()
    original = cv2.imread(args.f)
    thickened = preprocess_image(original)
    find_rectangles(original, thickened)
