import sys
import argparse

parser = argparse.ArgumentParser(description = 
        """
        Calculates score (precision and recall) on autentic rectangles' classes and predicted ones.
        Input: stdin input of two columns separated by whitespace.
        """
        )
parser.add_argument("-t", help = "Threshold", type = float, required = True)
args = parser.parse_args()


def calculate_score():
    precision_numerator = 0
    precision_denominator = 0

    recall_numerator = 0
    recall_denominator = 0
    for line in sys.stdin:
        p, t = [float(x) for x in line.strip().split()]
        if p >= args.t and t == 1:
            precision_numerator += 1
            recall_numerator += 1
        if p >= args.t:
            precision_denominator += 1
        if t == 1:
            recall_denominator += 1

    if precision_denominator == 0:
        precision = "N/A"
    else:
        precision = str(float(precision_numerator) / precision_denominator)
    if recall_denominator == 0:
        recall = "N/A"
    else:
        recall = str(float(recall_numerator) / recall_denominator)


    print("Precision = " + precision)
    print("Recall = " + recall)



if __name__ == "__main__":
    calculate_score()
