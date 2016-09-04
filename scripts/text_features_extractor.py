#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Prints text features of the given rectangle,                                                                                                                                                  
   each xml given as stdin should be cleaned by wrong_chars_xml_cleaner                                                                                                                         
   as the positional argument must be given .rect file                                                                                                                                           
"""

import sys
import re
import xml.etree.ElementTree as ET
import string
import argparse
import kenlm
from collections import OrderedDict

parser = argparse.ArgumentParser(description="Extractor of text features included in .xml file od djvu format")
parser.add_argument('-pc', help="filename where coordinates are kept.")
args = parser.parse_args()

tree_xml = ""
for line in sys.stdin: tree_xml += line
root = ET.fromstring(tree_xml)

def cut_xml(_x1, _y1, _x2, _y2):
    """Returns words which are in rectangle (based on given xml)
       Parameters:
       ----------
       _x1, _y1, _x2, _y2 : coordinates of rectangle
    """
    words_list = []
    for word in root.iter('WORD'):
        if word.text is not None: 
            coordinates = list(word.attrib.values())[0].split(',')                                                                  
            x1 = coordinates[0]                                                                                                                     
            y1 = coordinates[1]                  
            x2 = coordinates[2]                                                                                                                     
            y2 = coordinates[3]
        if (int(x1) > _x1 and int(x2) < _x2 and int(y1) > _y1 and int(y2) < _y2 and word.text is not None): 
            words_list.append(word.text.rstrip().lstrip())
    return words_list

def get_chars_amount(words_list):
    """Returns number of chars in rectangle
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    return sum([len(word) for word in words_list])

def get_punct_amount(words_list):
    """Returns number of punctation in rectangle
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
    return sum([count(word, string.punctuation) for word in words_list])

def get_words_amount(words_list):
    """Returns number of words in rectangle
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    return len(words_list)

def get_letters_amount(chars_counter, punct_counter):
    """Returns diff between chars amount and punctation amount,
       counts how many letters we have.
       Parameters:
       ----------
       chars_counter : tells about number of chars
       punct_counter : tells about number of punctation
    """
    if (chars_counter - punct_counter < 0): return 0
    else : return chars_counter - punct_counter

def get_vowels_consonants_amount(words_list):
    """Returns vowels and consonants number in rectangle
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    vowel_counter = 0
    consonants_counter = 0
    for word in words_list:
        for letter in word:
            if letter in "aeiouyąęó" : vowel_counter += 1
            elif (letter not in "aeiouyąęó" and letter.isalpha()): consonants_counter += 1
    return vowel_counter, consonants_counter

def get_numbers_amount(words_list):
    """Returns amount of numbers in rectangle
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    digit_counter = 0
    for word in words_list:
        for letter in word:
            if letter.isdigit(): digit_counter += 1
    return digit_counter

def get_lm_score(words_list):
    """Returns logarythmic scaled probability of sentence from LM
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    necrologue_lm = kenlm.LanguageModel("LM/necrologies_lm.klm")
    return necrologue_lm.score(" ".join(words_list))

def remove_special_characters(words_list):
    """ Returns list with replaced vw special characters                                                                                                                                        
        Parameters:                                                                                                                                                                              
        ----------                                                                                                                                                                               
        words_list : list of words generated from cut_xml() function                                                                                                                             
    """
    sentence_h = list(" ".join(words_list))
    sentence = []
    for char in sentence_h:
        char = char.replace(":","COLON").replace("|", "PIPE").replace(" ", "SPACE")
        sentence.append(char)
    return sentence
    
def get_trigrams(words_list):
   """Returns chars trigrams
      Parameters:
      ----------
      words_list : list of words generated from cut_xml() function
   """
   sentence = remove_special_characters(words_list)
   trigrams = []
   if len(sentence) >= 3:
       index = 0
       while index < len(sentence) - 2:
           trigrams.append("TRIGRAM+" + str(sentence[index]) + str(sentence[index + 1]) + str(sentence[index + 2]))
           index += 1
            
   return " ".join(trigrams)

def get_unigrams(words_list):
    """Returns chars unigrams
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    sentence = remove_special_characters(words_list)
    unigrams = ["CHAR+" + letter for letter in sentence]
    return " ".join(unigrams)

def get_bigrams(words_list):
    """Returns chars bigrams
       Parameters:
       ----------
       words_list : list of words generated from cut_xml() function
    """
    sentence = remove_special_characters(words_list)
    bigrams = []
    if len(sentence) >= 2:
        index = 0
        while index < len(sentence) - 1:
            bigrams.append("BIGRAM+" + str(sentence[index]) + str(sentence[index + 1]))
            index += 1
    return " ".join(bigrams)
              
if __name__ == "__main__":
    coords_input = []
    with open(args.pc) as coords:
        for coord in coords.readlines(): 
            coords_input.append(coord.replace(":","").replace("X1","").replace("X2","").replace("X3","").replace("X4","")\
                                .replace("Y1","").replace("Y2","").replace("Y3","").replace("Y4","").rstrip().split(" "))
    for coord_input in coords_input :
        text_feature = OrderedDict()
        words_list = cut_xml(int(coord_input[0]),int(coord_input[1]),int(coord_input[2]),int(coord_input[3]))
######## NUMBER FEATURES
        text_feature["CHARS_AMOUNT:"] = get_chars_amount(words_list)
        text_feature["WORDS_AMOUNT:"] = get_words_amount(words_list)
        text_feature["PUNCT_AMOUNT:"] = get_punct_amount(words_list)
        text_feature["LETTERS_AMOUNT:"] = get_letters_amount(text_feature["CHARS_AMOUNT:"], text_feature["PUNCT_AMOUNT:"])
        text_feature["VOWELS_AMOUNT:"], text_feature["CONSONANTS_AMOUNT:"] = get_vowels_consonants_amount(words_list)
        text_feature["DIGITS_AMOUNT:"] = get_numbers_amount(words_list)
        text_feature["LM_SCORE:"] = get_lm_score(words_list)
######## STRING FEATURES
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
