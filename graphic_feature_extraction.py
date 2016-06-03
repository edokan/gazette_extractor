import sys
import cv2
import argparse
from collections import OrderedDict
import numpy as np
from detect_peaks import detect_peaks

parser = argparse.ArgumentParser(description = "")
parser.add_argument("-f", help = "Page image input", required = True)
parser.add_argument("-v", help = "Verbose mode", action = 'store_true', default = False)
parser.add_argument("-n", help = "Take every h pixel to count peaks and valleys", type = int, default = 2)
args = parser.parse_args()

features = OrderedDict()


def histograms(roi):
    height, width = roi.shape
    horizontal = []
    vertical = []

    horizontal_hist = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
    vertical_hist = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
    
    for i in range(height):
        value = width - cv2.countNonZero(roi[i, :])
        if value == width:
            value = width - 1
        vertical.append(value)
        vertical_hist[i][value] = [0, 0, 255] 
        if i == 0:
            before = (value, i)
        else:
            cv2.line(vertical_hist, before, (value, i), (0, 0, 255), 2)
            before = (value, i)

    for i in range(width):
        value = height - cv2.countNonZero(roi[:, i])
        if value == height:
            value = height - 1
        horizontal.append(value)
        horizontal_hist[value][i] = [255, 0, 0] 
        if i == 0:
            before = (i, value)
        else:
            cv2.line(horizontal_hist, before, (i, value), (255, 0, 0), 2)
            before = (i, value)

    ############# HISTOGRAM PEAKS AND VALLEYS #######################################33
    
    every = args.n

    horizontal_less = horizontal[0::every]
    vertical_less = vertical[0::every]

    ### VALLEYS ###

    horizontal_valleys = detect_peaks(horizontal_less, mph=None, mpd=10, threshold=0, edge='falling', kpsh=False, valley=True, show=False, ax=None)
    for i in range(len(horizontal_valleys)):
        cv2.line(horizontal_hist, (horizontal_valleys[i] * every, horizontal[horizontal_valleys[i] * every]), (horizontal_valleys[i] * every, horizontal[horizontal_valleys[i] * every]), (255, 255, 0), 10)

    vertical_valleys = detect_peaks(vertical_less, mph=None, mpd=10, threshold=0, edge='falling', kpsh=False, valley=True, show=False, ax=None)
    for i in range(len(vertical_valleys)):
        cv2.line(vertical_hist, (vertical[vertical_valleys[i] * every], vertical_valleys[i] * every), (vertical[vertical_valleys[i] * every], vertical_valleys[i] * every), (255, 255, 0), 10)

    ### PEAKS ###
    
    horizontal_peaks = detect_peaks(horizontal_less, mph=None, mpd=10, threshold=0, edge='falling', kpsh=False, valley=False, show=False, ax=None)
    for i in range(len(horizontal_peaks)):
        cv2.line(horizontal_hist, (horizontal_peaks[i] * every, horizontal[horizontal_peaks[i] * every]), (horizontal_peaks[i] * every, horizontal[horizontal_peaks[i] * every]), (0, 255, 0), 10)

    vertical_peaks = detect_peaks(vertical_less, mph=None, mpd=10, threshold=0, edge='falling', kpsh=False, valley=False, show=False, ax=None)
    for i in range(len(vertical_peaks)):
        cv2.line(vertical_hist, (vertical[vertical_peaks[i] * every], vertical_peaks[i] * every), (vertical[vertical_peaks[i] * every], vertical_peaks[i] * every), (0, 255, 0), 10)

    ### SHOW HISTOGRAMS IN VERBOSE MODE ###

    features["HORIZONTAL_PEAKS"] = str(len(horizontal_peaks))
    features["HORIZONTAL_VALLEYS"] = str(len(horizontal_valleys))
    features["VERTICAL_PEAKS"] = str(len(vertical_peaks))
    features["VERTICAL_VALLEYS"] = str(len(vertical_valleys))


    if args.v:
        cv2.imshow('horizontal', horizontal_hist)
        cv2.imshow('vertical', vertical_hist)
        cv2.waitKey()


def calculate_filled(roi, height, width):
    all_pixels = height * width
    white_pixels = cv2.countNonZero(roi)
    black_pixels = all_pixels - white_pixels 
    filled = float(black_pixels) / all_pixels
    return filled


def analyze_rectangle(page, rectangle):
    x1, y1, x2, y2 = rectangle
    roi = page[y1:y2 + 1, x1:x2 + 1]
    height, width = roi.shape

    filled = calculate_filled(roi, height, width)


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
        x1, y1, x2, y2 = [int(x.split(":")[1]) for x in line.strip().split()]
        rectangles.append((x1, y1, x2, y2))

    image = cv2.imread(args.f, 0) 
    otsu_value, page = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV - cv2.THRESH_OTSU)

    for rectangle in rectangles:
        analyze_rectangle(page, rectangle)
        print_features()


