#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Prints text features of the given rectangle,
each xml given as stdin should be cleaned by xml_cleaner
"""

import sys
import re
import xml.etree.ElementTree as ET
import string
import argparse
import kenlm
from collections import OrderedDict
from common_text_features_functions import *

def get_chars_amount(words_list):
    """
    Returns number of chars in desired rectangle.

    Args:
        words_list (list) : list of words from rectangle
    """

    return sum([len(word) for word in words_list])

def get_words_amount(words_list):
    """
    Returns number of words in desired rectangle.

    Args:
        words_list (list) : list of words from rectangle
    """
    return len(words_list)

def get_letters_amount(chars_counter, punct_counter):
    """
    Returns diff between chars amount and punctation amount, counts how many letters we have.

    Args:
        chars_counter (int) : tells about number of chars
        punct_counter (int) : tells about number of punctation
    """

    if (chars_counter - punct_counter < 0): return 0
    else : return chars_counter - punct_counter

def get_vowels_consonants_amount(words_list):
    """
    Returns diff bvowels and consonants numer in rectangle.

    Args:
        words_list (list) : list of words from rectangle
    """
    vowel_counter = 0
    consonants_counter = 0
    for word in words_list:
        for letter in word:
            if letter in "aeiouyąęó" : vowel_counter += 1
            elif (letter not in "aeiouyąęó" and letter.isalpha()): consonants_counter += 1
    return vowel_counter, consonants_counter

def get_numbers_amount(words_list):
    """
    Returns amount of numers in rectangle.

    Args:
        words_list (list) : list of words from rectangle
    """

    digit_counter = 0
    for word in words_list:
        for letter in word:
            if letter.isdigit(): digit_counter += 1
    return digit_counter

def remove_special_characters(words_list):
    """
    Returns sentence with replaced special characters from vowpal wabbit ( " " -> "SPACE", ":" -> "COLON", "|" -> "PIPE").

    Args:
        words_list (list) : list of words from rectangle
    """
    sentence_h = list(" ".join(words_list))
    sentence = []
    for char in sentence_h:
        char = char.replace(":","COLON").replace("|", "PIPE").replace(" ", "SPACE")
        sentence.append(char)
    return sentence
    
def get_trigrams(words_list):
    """
    Returns char trigrams.

    Args:
        words_list (list) : list of words from rectangle
    """
    sentence = remove_special_characters(words_list)
    trigrams = []
    if len(sentence) >= 3:
        index = 0
        while index < len(sentence) - 2:
            trigrams.append("TRIGRAM+" + str(sentence[index]).lower() + str(sentence[index + 1]).lower() + str(sentence[index + 2]).lower())
            index += 1
            
    return " ".join(trigrams)

def get_bigrams(words_list):
    """
    Returns char bigrams.

    Args:
        words_list (list) : list of words from rectangle
    """
    sentence = remove_special_characters(words_list)
    bigrams = []
    if len(sentence) >= 2:
        index = 0
        while index < len(sentence) - 1:
            bigrams.append("BIGRAM+" + str(sentence[index]).lower() + str(sentence[index + 1]).lower())
            index += 1
    return " ".join(bigrams)

def get_unigrams(words_list):
    """
    Returns char unigrams.

    Args:
        words_list (list) : list of words from rectangle
    """
    sentence = remove_special_characters(words_list)
    unigrams = ["CHAR+" + letter.lower() for letter in sentence]
    return " ".join(unigrams)


if __name__ == "__main__":
    coords_input = []

    parser = argparse.ArgumentParser(description="Extractor of text features included in .xml file od djvu format")
    parser.add_argument('-pc', help="filename where coordinates are kept.")
    parser.add_argument('-xc', help="xml_coord")
    args = parser.parse_args()

    with open(args.pc) as coords:
        for coord in coords.readlines(): 
            coords_input.append(coord.replace(":","").replace("X1","").replace("X2","").replace("X3","").replace("X4","")\
                                .replace("Y1","").replace("Y2","").replace("Y3","").replace("Y4","").rstrip().split(" "))

    with open(args.xc) as xml_coord_file:
        xml_file = xml_coord_file.readlines()

    for coord_input in coords_input :
        text_feature = OrderedDict()
        words_list = cut_xml(coord_input[0], coord_input[1], coord_input[2], coord_input[3], xml_file)
        #NUMERIC FEATURES
        text_feature["CHARS_AMOUNT:"] = get_chars_amount(words_list)
        text_feature["WORDS_AMOUNT:"] = get_words_amount(words_list)
        text_feature["PUNCT_AMOUNT:"] = get_punct_amount(words_list)
        text_feature["LETTERS_AMOUNT:"] = get_letters_amount(text_feature["CHARS_AMOUNT:"], text_feature["PUNCT_AMOUNT:"])
        text_feature["VOWELS_AMOUNT:"], text_feature["CONSONANTS_AMOUNT:"] = get_vowels_consonants_amount(words_list)
        text_feature["DIGITS_AMOUNT:"] = get_numbers_amount(words_list)
        #STRING FEATURES
        text_feature[get_trigrams(words_list)] = ""
        text_feature[get_bigrams(words_list)] = ""
        text_feature[get_unigrams(words_list)] = ""

        for feature in text_feature:
            if text_feature[feature] == "":
                sys.stdout.write(feature + " ")
            else:
                sys.stdout.write(feature + str(text_feature[feature]) + " ")
            sys.stdout.flush()
        sys.stdout.write("\n")

