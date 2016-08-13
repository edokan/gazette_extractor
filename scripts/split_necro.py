import sys
import argparse

parser = argparse.ArgumentParser(
        description = 
        """
        Split obituaries in expected.tsv to separate files based on in.tsv.
        """
        )
parser.add_argument("-i", help = "File in.tsv")
parser.add_argument("-e", help = "File expected.tsv")
parser.add_argument("-o", help = "Output directory")
args = parser.parse_args()

if __name__ == "__main__":
    with open(args.i) as in_file, open(args.e) as expected_file:
        for in_line, expected_line in zip(in_file, expected_file):
            filename = args.o + "/" + in_line.rstrip(".djvu\n") + ".necro"
            with open(filename, 'w') as necro_file:
                necro_file.write(expected_line.strip() + "\n")



