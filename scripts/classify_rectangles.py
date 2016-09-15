import sys
import argparse
import cv2
from collections import OrderedDict

parser = argparse.ArgumentParser(description = 
        """
        Tags generated rectangles using information stored in necro file.
        If there is necrology on page and there's no corresponding rectangle, it's appended to rectangle file.
        """
        )
parser.add_argument("-n", help = "File with necro coordinates", required = True)
parser.add_argument("-r", help = "File with generated rectangles", required = True)
parser.add_argument("-i", help = "Page number", type = int, required = True)
parser.add_argument("-e", help = "Tolerance error", type = int, default = 50)
args = parser.parse_args()

rectangles = OrderedDict()
necrologies = []


def load_rectangles():
    """
    Loads rectangles' coordinates from file.
    """
    with open(args.r, 'r') as f:
        for line in f:
            x1, y1, x2, y2 = [int(c.split(":")[1]) for c in line.strip().split()]
            rectangles[(x1, y1, x2, y2)] = -1


def load_necrologies():
    """
    Load necrologies' coordinates from file.
    """

    with open(args.n, 'r') as f:
        line = f.readline().strip()
        for necro in line.split():
            page, coordinates = necro.split("/")
            x1, y1, x2, y2 = [int(n) for n in coordinates.split(",")]
            necrologies.append((int(page), x1, y1, x2, y2))


def check_error(necrology, rectangle):
    """
    Check coordinates of rectangle error (how near it is to necrology).
    Return error value of all 4 nodes.
    """
    
    n_page, n_x1, n_y1, n_x2, n_y2 = necrology
    r_x1, r_y1, r_x2, r_y2 = rectangle

    error = 0
    error += abs(n_x1 - r_x1)
    error += abs(n_y1 - r_y1)
    error += abs(n_x2 - r_y2)
    error += abs(n_y2 - r_y2)

    return error

def classify():
    """
    Tag all rectangles with classes based on necrologies' coordinates.
    """

    modified = False
    for necro in necrologies:
        # print >> sys.stderr, "NECRO: " + str(necro)
        page, x1, y1, x2, y2 = necro
        if page != args.i:
            continue
        found = False
        rect_error = {}
        for rec in rectangles:
            rect_error[rec] = check_error(necro, rec)
            nearest = min(rect_error, key=rect_error.get)
            # print >> sys.stderr, rect_error[nearest]
            # print >> sys.stderr, float(rect_error[nearest]) / 4
        if float(rect_error[nearest]) / 4 < float(args.e):
            # print >> sys.stderr, "FOUND IT"
            rectangles[nearest] = 1
            found = True
        if not found:
            rectangles[necro[1:]] = 1
            modified = True
    return modified


def modify_rectangle_file(modified):
    """
    If any necrology is not found in rectangles, rectangle file is modified.
    """
    
    if modified:
        print >> sys.stderr, "MODIFIED!"
        with open(args.r, 'w') as f:
            for rect in rectangles:
                x1, y1, x2, y2 = rect
                output = ["X1:" + str(x1), "Y1:" + str(y1), 
                          "X2:" + str(x2), "Y2:" + str(y2)]
                f.write(" ".join(output) + '\n')


if __name__ == "__main__":
    load_rectangles()
    load_necrologies()
    modified = classify()
    modify_rectangle_file(modified)

    for rect in rectangles:
        print(rectangles.get(rect, -1))

