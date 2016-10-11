"""
Script to map extracted obituaries in order of DJVU files.
"""

import sys
import argparse

necrologies = {}


def parse_args():
    """
    Parse command line arguments.
    """

    parser = argparse.ArgumentParser(description="""
                        Map extracted obituaries by in.tsv order.
                        """
                                     )
    parser.add_argument("-i", help="Path to in.tsv file.", required=True)
    return parser.parse_args()


def load_input():
    """
    Load extracted necrologies from stdin.
    """

    for line in sys.stdin:
        djvu, necro = line.strip().split("\t")
        if necro == "NULL":
            necro = ""
        necrologies[djvu] = necro


def map_output(i_file):
    """
    Map extracted necrologies by filenames order in.tsv file.

    Args:
        i_file (str): Path to in.tsv file.
    """

    with open(i_file) as in_file:
        for line in in_file:
            djvu = line.strip()
            print(necrologies[djvu])


if __name__ == "__main__":
    args = parse_args()
    load_input()
    map_output(args.i)
