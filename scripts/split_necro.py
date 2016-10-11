"""
Split training data into seperate files (each for DDJVU file).
"""

import argparse
import os.path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Split obituaries in train.tsv to separate files for multiprocessing.
            """
                                     )
    parser.add_argument("-i", help="Input file train.tsv")
    parser.add_argument("-o", help="Output directory")
    args = parser.parse_args()

    with open(args.i) as in_file:
        for in_line in in_file:
            necros = ""
            splitted = in_line.split("\t")
            if len(splitted) == 1:
                djvu = splitted[0].strip()
            else:
                djvu = splitted[0].strip()
                necros = splitted[1].strip()

            filename = args.o + "/" + djvu.replace(".djvu", ".necro")
            if not os.path.exists(filename):
                with open(filename, 'w') as necro_file:
                    necro_file.write(necros + "\n")
