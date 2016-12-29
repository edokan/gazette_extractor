import sys
import argparse
from collections import OrderedDict


class Classifier:
    """
    Classify each rectangle if it's obituary or not based on training data.

    Note:
        If Classifier does not find obituary, it adds it to already generated rectangles.
    """

    def __init__(self, r_file, n_file, page, error):
        self.rectangles = OrderedDict()
        self.necrologies = []
        self.load_rectangles(r_file)
        self.load_necrologies(n_file)
        modified = self.classify(page, error)
        self.modify_rectangle_file(r_file, modified)

        for rect in self.rectangles:
            print(self.rectangles.get(rect, -1))

    def load_rectangles(self, r_file):
        """
        Loads rectangles' coordinates from file.

        Args:
            r_file (str): Path to file with rectangles' coordinates.
        """

        with open(r_file, 'r') as f:
            for line in f:
                x1, y1, x2, y2 = [int(c.split(":")[1]) for c in line.strip().split()]
                self.rectangles[(x1, y1, x2, y2)] = -1

    def load_necrologies(self, n_file):
        """
        Load necrologies' coordinates from file.

        Args:
            n_file (str): Path to file with necrologies' coordinates.
        """

        with open(n_file, 'r') as f:
            line = f.readline().strip()
            for necro in line.split():
                page, coordinates = necro.split("/")
                x1, y1, x2, y2 = [int(n) for n in coordinates.split(",")]
                self.necrologies.append((int(page), x1, y1, x2, y2))

    def check_error(self, necrology, rectangle):
        """
        Check coordinates of rectangle error (how near it is to necrology).
        Return error value of all 4 nodes.

        Args:
            necrology (tuple): coordinates of compared necrology.
            rectangle (tuple): coordinates of compared rectangle.
        """

        n_page, n_x1, n_y1, n_x2, n_y2 = necrology
        r_x1, r_y1, r_x2, r_y2 = rectangle
        error = 0
        error += abs(n_x1 - r_x1)
        error += abs(n_y1 - r_y1)
        error += abs(n_x2 - r_y2)
        error += abs(n_y2 - r_y2)
        return error

    def classify(self, page, error):
        """
        Tag all rectangles with classes based on necrologies' coordinates.

        Args:
            i (int): Page number.
        """

        modified = False
        for necro in self.necrologies:
            # print >> sys.stderr, "NECRO: " + str(necro)
            i, x1, y1, x2, y2 = necro
            if i != page:
                continue
            found = False
            rect_error = {}
            for rec in self.rectangles:
                rect_error[rec] = self.check_error(necro, rec)
            try:
                nearest = min(rect_error, key=rect_error.get)
                # print >> sys.stderr, rect_error[nearest]
                # print >> sys.stderr, float(rect_error[nearest]) / 4
                # print >> sys.stderr, str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2)
                if float(rect_error[nearest]) / 4 < float(error):
                    # print >> sys.stderr, "FOUND IT"
                    self.rectangles[nearest] = 1
                    found = True
            except ValueError:
                pass
            if not found:
                self.rectangles[necro[1:]] = 1
                modified = True
        return modified

    def modify_rectangle_file(self, r_file, modified):
        """
        If any necrology is not found in rectangles, rectangle file is modified.

        Args:
            modified (bool): flag that checks if rectangle file should be modified.
        """

        if modified:
            print >> sys.stderr, "MODIFIED!"
            with open(r_file, 'w') as f:
                for rect in self.rectangles:
                    x1, y1, x2, y2 = rect
                    output = ["X1:" + str(x1), "Y1:" + str(y1),
                              "X2:" + str(x2), "Y2:" + str(y2)]
                    f.write(" ".join(output) + '\n')


def parse_args():
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(description="""
            Tags generated rectangles using information stored in necro file.
            If there is necrology on page and there's no corresponding rectangle,
            it's appended to rectangle file.
            """
                                     )
    parser.add_argument("-n", help="File with necro coordinates", required=True)
    parser.add_argument("-r", help="File with generated rectangles", required=True)
    parser.add_argument("-i", help="Page number", type=int, required=True)
    parser.add_argument("-e", help="Tolerance error", type=int, default=400)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    classifier = Classifier(args.r, args.n, args.i, args.e)
