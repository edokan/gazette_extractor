import sys
import cv2
import argparse
import os


class RectangleGenerator():
    """
    This class preprocesses page image, so it can find coordinates
    of potential obituaries.

    Args:
        f_path (string): Path to page image.
        l (int): Lower bound of possible rectangle.
        u (int): Upper bound of possible rectangle.
        verbose (bool): Verbose mode.
    """

    def __init__(self, f_path, l, u, verbose):
        self.paragraphs = []
        self.lines = []
        self.words = []
        self.load_coordinates()
        self.original = cv2.imread(f_path)
        self.thickened = self.preprocess_image()
        self.rectangles = self.find_rectangles(l, u, verbose)
        self.filtered_rect = self.remove_duplicates()
        self.print_rectangles()

    def load_coordinates(self):
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
                self.paragraphs.append(coordinates)
            elif data_type == "LINE":
                self.lines.append(coordinates)
            elif data_type == "WORD":
                self.words.append(coordinates)
            else:
                continue

    def remove_words(self, image):
        """
        Cover words on image with filled rectanges.

        Args:
            image (matrix): Image to cover its words.
        """

        for coord in self.words:
            x1, y1, x2, y2 = coord
            cv2.rectangle(image, (x1, y1), (x2, y2), 0, thickness=-1)

    def preprocess_image(self):
        """
        Preprocess page image to find rectangles.
        """

        image = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)

        # Thresholding
        otsu_value, thresholded = cv2.threshold(
            image, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Cover words
        self.remove_words(thresholded)

        # Thicken skeleton
        thickened = cv2.dilate(thresholded, cv2.getStructuringElement(
            cv2.MORPH_RECT, (7, 7)), iterations=1)

        return thickened

    def check_if_near(self, a, b):
        """
        Check if two rectangles are near each other.

        Args:
            a (tuple): First rectangle.
            b (tuple): Second rectangle.
        """

        x1_a, y1_a, x2_a, y2_a = a
        x1_b, y1_b, x2_b, y2_b = b

        x1_a_b = float(x1_a) / x1_b
        x1_b_a = float(x1_b) / x1_a
        y1_a_b = float(y1_a) / y1_b
        y1_b_a = float(y1_b) / y1_a
        x2_a_b = float(x2_a) / x2_b
        x2_b_a = float(x2_b) / x2_a
        y2_a_b = float(y2_a) / y2_b
        y2_b_a = float(y2_b) / y2_a

        gt_1 = [y1_a_b, x2_a_b]
        lt_1 = [x1_a_b, y2_a_b]

        errors = [min(x1_a_b, x1_b_a),
                  min(y1_a_b, y1_b_a),
                  min(x2_a_b, x2_b_a),
                  min(y2_a_b, y2_b_a)]

        # sys.stderr.write(str(a) + " | " + str(b))
        # sys.stderr.write("\n")
        # for e in errors:
            # sys.stderr.write(str(e) + " ")
        # sys.stderr.write("\n")

        if sum(e >= 0.8 for e in errors) >= 2:
            gt = sum(g >= 1 for g in gt_1)
            lt = sum(l < 1 for l in lt_1)
            if gt + lt >= 2:
                return True, a
            else:
                return True, b
        else:
            return False, []

    def remove_duplicates(self):
        """
        Filter generated rectangles from potential duplicates.
        """

        result = []
        duplicates = set()
        for a in self.rectangles:
            if a in duplicates:
                continue
            found = False
            for b in self.rectangles:
                if a == b:
                    continue
                is_close, bigger = self.check_if_near(a, b)
                if is_close and not found:
                    result.append(bigger)
                    duplicates.add(b)
                    found = True
            if not found:
                result.append(a)
        return result

    def print_rectangles(self):
        """
        Print generated rectangles.
        """

        for x1, y1, x2, y2 in self.filtered_rect:
            rectangle = {"X1": str(x1),
                         "Y1": str(y1),
                         "X2": str(x2),
                         "Y2": str(y2)}
            for param in ["X1", "Y1", "X2", "Y2"]:
                sys.stdout.write(param + ":" + str(rectangle[param]) + " ")
            sys.stdout.write("\n")

    def find_rectangles(self, l, u, verbose):
        """
        Find potential necrology coordinates and print them.

        Args:
            l (int): Lower bound of potential rectangles.
            u (int): Upper bound of potential rectangles.
            verbose (bool): Verbose mode.
        """

        rectangles = []
        contours, hierarchy = cv2.findContours(
            self.thickened.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
        # unimportant_rect = set()

        for i, cnt in enumerate(contours):
            # if hierarchy[0, i, 3] == -1:
            x, y, w, h = cv2.boundingRect(cnt)
            x1, y1, x2, y2 = x, y, x + w, y + h
            roi = self.original[y1:y2 + 1, x1:x2 + 1]
            height, width, channels = roi.shape
            if (height > l and width > l) and (height < u and width < u):
                # if hierarchy[0, i, 3] == -1 or (i in unimportant_rect):
                rectangles.append((x, y, x + w, y + h))
            # else:
                # unimportant_rect.add(i)

        if verbose:
            rect_image = self.original.copy()
            rect_output = args.f.replace(".tiff", ".rect.tiff")
            skel_output = args.f.replace(".tiff", "skel.tiff")
            rect_dir = args.f.replace(".tiff", "")
            if not os.path.exists(rect_dir):
                os.makedirs(rect_dir)

            enum = 0
            for x1, y1, x2, y2 in rectangles:
                height = y2 - y1
                width = x2 - x1
                filename = rect_dir + "/" + str(x1) + "_" + str(y1) + \
                    "_" + str(x2) + "_" + str(y2) + ".tiff"
                cv2.imwrite(filename, self.original[y1:y2 + 1, x1:x2 + 1])
                enum += 1
                cv2.rectangle(rect_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

            cv2.imwrite(rect_output, rect_image)
            cv2.imwrite(skel_output, self.thickened)
        return rectangles


def parse_args():
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(description="""
            Generates potential necrology rectangles.
            """
                                     )
    parser.add_argument("-f", help="Path to page image.", required=True)
    parser.add_argument("-l", help="Lower bound of possible rectangle", type=int, required=True)
    parser.add_argument("-u", help="Upper bound of possible rectangle", type=int, required=True)
    parser.add_argument("-v", help="Verbose mode", action='store_true', default=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    generator = RectangleGenerator(args.f, args.l, args.u, args.v)
