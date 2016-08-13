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
            page, coordinates, error = necro.split("/")
            x1, y1, x2, y2 = [int(n) for n in coordinates.split(",")]
            necrologies.append((int(page), x1, y1, x2, y2, int(error)))


def check_if_near(necrology, rectangle):
    """
    Check if coordinates of rectangle are near enough a necrology.
    If so, we tag rectangle as necrology.
    """
    
    n_page, n_x1, n_y1, n_x2, n_y2, error = necrology
    r_x1, r_y1, r_x2, r_y2 = rectangle

    if (n_x1 - error <= r_x1 <= n_x1 + error and
        n_y1 - error <= r_y1 <= n_y1 + error and
        n_x2 - error <= r_x2 <= n_x2 + error and
        n_y2 - error <= r_y2 <= n_y2 + error):
        return True
    else:
        return False

def classify():
    """
    Tag all rectangles with classes based on necrologies coordinates.
    """

    modified = False
    for necro in necrologies:
        page, x1, y1, x2, y2, error = necro
        if page != args.i:
            continue
        found = False
        for rec in rectangles:
            if check_if_near(necro, rec):
                rectangles[rec] = 1
                found = True
                break
        if not found:
            rectangles[necro[1:-1]] = 1
            modified = True
    return modified


def modify_rectangle_file(modified):
    """
    If any necrology is not found in rectangles, rectangle file is modified.
    """
    
    if modified:
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

