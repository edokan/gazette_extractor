#!/usr/bin/python3                                                                                                                                                                               # -*- coding: utf-8 -*-
"""
Script which:
- calculates lm score of rectangle based on necrologies language model.
- calculates lm of page based on pages with necrologies language model. Used with BPE.
"""

import sys, os
sys.path.insert(0, os.getcwd() + "/scripts/subword-nmt")
import re
import xml.etree.ElementTree as ET
import argparse
import kenlm
from apply_bpe import BPE
from common_text_features_functions import cut_xml

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Applying LM for the gazette.")
    parser.add_argument('-vw', help="VW file without calculated lm -> gazettetitle.without_lm.vw")
    parser.add_argument('--codes', '-c', type=argparse.FileType('r'), help="File with BPE codes (created by learn_bpe.py).")
    args = parser.parse_args()

    #Define lm
    pages_lm = kenlm.LanguageModel("LM/necrologies_lm.klm")
    necrologues_lm = kenlm.LanguageModel("LM/necrologies_lm.klm")

    bpe = BPE(args.codes, "@@")

    vw_file = args.vw
    file_name = os.path.basename(vw_file)
    gazette_title = vw_file.replace(file_name, "")

    with open(vw_file) as rectangles_to_check:
        for rectangle in rectangles_to_check.readlines():
            page = re.search(r"PAGE:\d\d?", rectangle).group(0).replace("PAGE:","")
            x1 = re.search(r"X1:\d{1,4}", rectangle).group(0).replace("X1:","")
            x2 = re.search(r"X2:\d{1,4}", rectangle).group(0).replace("X2:","")
            y1 = re.search(r"Y1:\d{1,4}", rectangle).group(0).replace("Y1:","")
            y2 = re.search(r"Y2:\d{1,4}", rectangle).group(0).replace("Y2:","")

            xml_coord = gazette_title + "/page_" + page + ".xml_coord"

            with open(xml_coord) as xml_coord_file:
                xml_coords = xml_coord_file.readlines()
            #LM for rectangle -> corpus of necrologue
            rectangle_text = cut_xml(x1, y1, x2, y2, xml_coords)
            rectangle_text_normalized = " ".join(rectangle_text).replace(""," ")[1: -1].lower()
            necro_lm_score = necrologues_lm.score(rectangle_text_normalized)
            sys.stdout.write("LM_RECT_SCORE:" + str(necro_lm_score) + " ")

            #LM for page which contains rectangle -> corpus of pages with necrologies 
            page_file = gazette_title + "/page_" + page.replace("PAGE:","") + ".txt"
            with open(page_file) as page_txt:
                bpe_text = bpe.segment((" ".join(page_txt.readlines())).lower().strip())
                page_lm_score = pages_lm.score(bpe_text)
                sys.stdout.write("LM_PAGE_SCORE:" + str(page_lm_score))
            
            sys.stdout.write("\n")
