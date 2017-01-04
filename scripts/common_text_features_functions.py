#!/usr/bin/python3                                                                                                                                                                              
# -*- coding: utf-8 -*-       

"""Module which contains functions which are used more than once in text features extraction scripts
"""

import xml.etree.ElementTree as ET
import string

def cut_xml(_x1, _y1, _x2, _y2, xml_file):
    """
    Returns text, contained in specified area (recognized rectangle in newspaper), from xml file.

    Args:
        _x1 (int) : Upper left-sided x coordinate
        _y1 (int) : Upper left-sided y coordinate
        _x2 (int) : Lower right-sided x coordinate
        _y2 (int) : Lower right-sided y coordinate
    """
    words = []
    for line in xml_file:
        type_of_line = line.split("\t")[0]
        if type_of_line == "WORD":
            line_data =line.split("\t")[1].split(" ")
            if len(line_data) >= 5:
                x1 = line_data[0]
                y1 = line_data[1]
                x2 = line_data[2]
                y2 = line_data[3]
                word = line_data[4]
                if (int(x1) > int(_x1) and int(x2) < int(_x2) and int(y1) > int(_y1) and int(y2) < int(_y2)):
                    words.append(word.strip())
    return(words)

def get_punct_amount(words_list):
    """
    Returns number of punctation in desired rectangle.

    Args:
        words_list (list) : list of words in which we need to check amount of punctation
    """

    count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
    return sum([count(word, string.punctuation) for word in words_list])
