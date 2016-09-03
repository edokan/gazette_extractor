import sys
import argparse

parser = argparse.ArgumentParser(description = 
        """
        Map extracted obituaries by in.tsv order.
        """
        )
parser.add_argument("-i", help = "File in.tsv", required = True)
args = parser.parse_args()

necrologies = {}

def load_input():
    for line in sys.stdin:
        djvu, necro = line.strip().split("\t")
        if necro == "NULL":
            necro = ""
        necrologies[djvu] = necro


def map_output():
    with open(args.i) as in_file:
        for line in in_file:
            djvu = line.strip()
            print(necrologies[djvu])


if __name__ == "__main__":
    load_input()
    map_output()
