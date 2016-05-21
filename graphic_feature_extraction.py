import sys
import cv2
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description = "")
parser.add_argument("-f", help = "Page image input")
parser.add_argument("-v", help = "Verbose mode", action = 'store_true', default = False)
args = parser.parse_args()

features = {}


def histograms(roi):
    height, width = roi.shape
    horizontal = []
    vertical = []

    roi_histograms = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
    
    for i in range(height):
        value = width - cv2.countNonZero(roi[i, :])
        if value == width:
            value = width - 1
        vertical.append(value)
        roi_histograms[i][value] = [0, 0, 255] 
        if i == 0:
            before = (value, i)
        else:
            cv2.line(roi_histograms, before, (value, i), (0, 0, 255), 2)
            before = (value, i)

    for i in range(width):
        value = height - cv2.countNonZero(roi[:, i])
        if value == height:
            value = height - 1
        horizontal.append(value)
        roi_histograms[value][i] = [255, 0, 0] 
        if i == 0:
            before = (i, value)
        else:
            cv2.line(roi_histograms, before, (i, value), (255, 0, 0), 2)
            before = (i, value)
    
    if args.v:
        cv2.imshow('histograms', roi_histograms)
        cv2.waitKey()


def analyze_rectangle(page, rectangle):
    x1, y1, x2, y2 = rectangle
    roi = page[x1:x2 + 1, y1:y2 + 1]
    height, width = roi.shape
    
    all_pixels = height * width
    white_pixels = cv2.countNonZero(roi)
    black_pixels = all_pixels - white_pixels 
    filled = float(black_pixels) / all_pixels
    
    # print(height, width, filled)
    features["HEIGHT"] = str(height)
    features["WIDTH"] = str(width)
    features["FILLED"] = str(filled)

    histograms(roi)


def print_features():
    for feature in features:
        sys.stdout.write(feature + ":" + features[feature] + "\t")
        sys.stdout.flush()
    sys.stdout.write("\n")

if __name__ == "__main__":
    rectangles = []
    for line in sys.stdin:
        x1, y1, x2, y2 = [int(x) for x in line.strip().split()]
        rectangles.append((x1, y1, x2, y2))

    page = cv2.imread(args.f, 0)
    for rectangle in rectangles:
        analyze_rectangle(page, rectangle)
        print_features()


