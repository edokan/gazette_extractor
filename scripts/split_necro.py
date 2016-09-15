import sys
import argparse
import os.path

parser = argparse.ArgumentParser(
        description = 
        """
        Split obituaries in train.tsv to separate files for multiprocessing.
        """
        )
parser.add_argument("-i", help = "Input file train.tsv")
parser.add_argument("-o", help = "Output directory")
args = parser.parse_args()

if __name__ == "__main__":
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



