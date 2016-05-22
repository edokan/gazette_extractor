import sys
import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser(description = "")
parser.add_argument("-f", help = "Page image input")
parser.add_argument("-s", type = int, help = "Number to split image to => A x A")
args = parser.parse_args()

if __name__ == "__main__":
    page = cv2.imread(args.f)
    height, width, colors = page.shape

    increment_i = height / args.s
    increment_j = width / args.s

    rest_i = height % increment_i
    rest_j = width % increment_j

    steps_h = range(0, height, increment_i)
    steps_h[-1] += rest_i

    steps_w = range(0, width, increment_j)
    steps_w[-1] += rest_j

    for i in range(len(steps_h) - 1):
        for j in range(len(steps_w) - 1):
            # rectangle = [steps_h[i], steps_w[j], steps_h[i + 1], steps_w[j + 1]]
            # print "\t".join([str(x) for x in rectangle])
            rectangle = {"X1":steps_h[i], "Y1":steps_w[j], "X2":steps_h[i + 1], "Y2":steps_w[j + 1]}
            for param in ["X1", "Y1", "X2", "Y2"]:
                sys.stdout.write(param + ":" + str(rectangle[param]) + "\t")
            sys.stdout.write("\n")
