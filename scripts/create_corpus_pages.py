#!/usr/bin/python3                                                                                                                                                                               
# -*- coding: utf-8 -*-  

"""Script which creates a corpora based on pages which contain necrologies. Normalization - lowercase.
"""
import sys
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract pages text which contain necrologies.")
    parser.add_argument('-fn', help="Filename where coordinates and page number of necrologue are kept. -> gazettetitle.necro")
    args = parser.parse_args()

    filename = args.fn
    gazette_title = filename.replace(".necro", "")
    necrologue = dict()

    with open(filename) as necrologues_data:
        for line in necrologues_data:
            for necrologue_data in line.split(" "):
                data = necrologue_data.split("/")
                if len(data) == 2 :
                    page = data[0]
                    
                page_with_necro = str(gazette_title) + "/page_" + str(page) + ".txt"

                with open(page_with_necro) as page_data:
                    for line in page_data:
                        sys.stdout.write(line.lower())
