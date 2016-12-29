import sys
import cv2
import argparse
from collections import OrderedDict
from detect_peaks import detect_peaks


class GraphicFeaturesExtractor():
    """
    Extract graphic features from generated rectangles.
    """

    def __init__(self, p_file, n, verbose):
        self.rectangles = []
        self.features = OrderedDict()
        self.load_rectangles()
        self.page = self.load_page(p_file)

        for rectangle in self.rectangles:
            self.analyze_rectangle(rectangle, n, verbose)
            self.print_features()
            self.features.clear()

    def histograms(self, roi, n, verbose):
        """
        Calculate horizontal and vertical histograms for a specified region of interest.

        Args:
            roi (matrix): region of interest cut from page.
            n (int): Consider every n pixel while searching for peaks.
            verbose (bool): verbose mode.
        """

        # CALCULATE HISTOGRAMS ###############################################

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

        # HISTOGRAM PEAKS AND VALLEYS #######################################

        horizontal_less = horizontal[0::n]
        vertical_less = vertical[0::n]

        # VALLEYS ###########################################################

        horizontal_valleys = detect_peaks(
            horizontal_less, mph=None, mpd=10, threshold=0, edge='falling', kpsh=False, valley=True, show=False, ax=None)
        for i in range(len(horizontal_valleys)):
            cv2.line(horizontal_hist, (horizontal_valleys[i] * n, horizontal[horizontal_valleys[
                     i] * n]), (horizontal_valleys[i] * n, horizontal[horizontal_valleys[i] * n]), (255, 255, 0), 20)

        vertical_valleys = detect_peaks(vertical_less, mph=None, mpd=10, threshold=0,
                                        edge='falling', kpsh=False, valley=True, show=False, ax=None)
        for i in range(len(vertical_valleys)):
            cv2.line(vertical_hist, (vertical[vertical_valleys[i] * n], vertical_valleys[i] * n),
                     (vertical[vertical_valleys[i] * n], vertical_valleys[i] * n), (255, 255, 0), 20)

        # PEAKS #############################################################

        horizontal_peaks = detect_peaks(horizontal_less, mph=None, mpd=10, threshold=0,
                                        edge='falling', kpsh=False, valley=False, show=False, ax=None)
        for i in range(len(horizontal_peaks)):
            cv2.line(horizontal_hist, (horizontal_peaks[i] * n, horizontal[horizontal_peaks[
                     i] * n]), (horizontal_peaks[i] * n, horizontal[horizontal_peaks[i] * n]), (0, 255, 0), 20)

        vertical_peaks = detect_peaks(vertical_less, mph=None, mpd=10, threshold=0,
                                      edge='falling', kpsh=False, valley=False, show=False, ax=None)
        for i in range(len(vertical_peaks)):
            cv2.line(vertical_hist, (vertical[vertical_peaks[i] * n], vertical_peaks[i] * n),
                     (vertical[vertical_peaks[i] * n], vertical_peaks[i] * n), (0, 255, 0), 20)

        # SHOW HISTOGRAMS IN VERBOSE MODE ##################################

        self.features["HORIZONTAL_PEAKS"] = str(len(horizontal_peaks))
        self.features["HORIZONTAL_VALLEYS"] = str(len(horizontal_valleys))
        self.features["VERTICAL_PEAKS"] = str(len(vertical_peaks))
        self.features["VERTICAL_VALLEYS"] = str(len(vertical_valleys))

        if verbose:
            cv2.imshow('horizontal', horizontal_hist)
            cv2.imshow('vertical', vertical_hist)
            cv2.waitKey()

    def calculate_filled(self, roi, height, width):
        """
        Calculate black fill percentage for a region of interest.

        Args:
            roi (matrix): region of interest cut from page.
            height (int): height of ROI.
            width (int): width of ROI.
        """

        all_pixels = height * width
        white_pixels = cv2.countNonZero(roi)
        black_pixels = all_pixels - white_pixels
        filled = float(black_pixels) / all_pixels
        return filled

    def analyze_rectangle(self, rectangle, n, verbose):
        """
        Analyze specific rectangle.

        Args:
            rectangle (tuple): coordinates of rectangle.
        """

        x1, y1, x2, y2 = rectangle
        roi = self.page[y1:y2 + 1, x1:x2 + 1]
        height, width = roi.shape

        filled = self.calculate_filled(roi, height, width)

        # print(height, width, filled)
        self.features["HEIGHT"] = str(height)
        self.features["WIDTH"] = str(width)
        self.features["FILLED"] = str(filled)

        self.histograms(roi, n, verbose)

    def print_features(self):
        """
        Print rectangle's features.
        """

        for feature in self.features:
            sys.stdout.write(feature + ":" + self.features[feature] + " ")
            sys.stdout.flush()
        sys.stdout.write("\n")

    def load_rectangles(self):
        """
        Load rectangles' coordinates from stdin.
        """

        for line in sys.stdin:
            x1, y1, x2, y2 = [int(x.split(":")[1]) for x in line.strip().split()]
            self.rectangles.append((x1, y1, x2, y2))

    def load_page(self, p_file):
        """
        Load page and threshold it.

        Args:
            p_file (str): Path to page image file.
        """

        image = cv2.imread(p_file, 0)
        otsu_value, page = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV - cv2.THRESH_OTSU)
        return page


def parse_args():
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(description="""
            Prints graphic features for list of rectangles' coordinates and page image.
            """
                                     )
    parser.add_argument("-f", help="Page image input", required=True)
    parser.add_argument("-v", help="Verbose mode", action='store_true', default=False)
    parser.add_argument(
        "-n", help="Take every n pixel to count peaks and valleys, default = 2", type=int, default=2)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    extractor = GraphicFeaturesExtractor(args.f, args.n, args.v)
