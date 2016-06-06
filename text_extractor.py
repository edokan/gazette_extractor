#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import xml.etree.ElementTree as ET
import string
import argparse

parser = argparse.ArgumentParser(description="Extractor of text features included in .xml file od djvu format")
parser.add_argument('p', help="Path to .xml file produced from djvu")
parser.add_argument('coordinates', help="Coordinates to cut it from file in single quote, whitespace separated")
args = parser.parse_args()

coord_input = args.coordinates.split(" ")

tree = ET.parse(args.p)
root = tree.getroot()

def cut_xml(_x1, _y1, _x2, _y2):
    words_list = []
    for word in root.iter('WORD'):
        if word is not None: 
            coordinates = list(word.attrib.values())[0].split(',')                                                                  
            x1 = coordinates[0]                                                                                                                     
            y1 = coordinates[1]                                                                                                                       
            x2 = coordinates[2]                                                                                                                       
            y2 = coordinates[3]
        if (int(x1) > _x1 and int(x2) < _x2 and int(y1) > _y1 and int(y2) < _y2 and word.text is not None): words_list.append(word.text)
    return words_list

def get_chars_amount(words_list):
    return sum([len(word) for word in words_list])

def get_punct_amount(words_list):
    count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
    return sum([count(word, string.punctuation) for word in words_list])

def get_words_amount(words_list):
    return len(words_list)

def get_letters_amount(chars_counter, punct_counter):
    if (chars_counter - punct_counter < 0): return 0
    else : return chars_counter - punct_counter

def get_vowels_consonants_amount(words_list):
    vowel_counter = 0
    consonants_counter = 0
    for word in words_list:
        for letter in word:
            if letter in "aeiouyóąę" : vowel_counter += 1
            elif (letter not in "aeiouyóąę" and letter.isalpha()): consonants_counter += 1
    return vowel_counter, consonants_counter

def main():

    words_list = cut_xml(int(coord_input[0]),int(coord_input[1]),int(coord_input[2]),int(coord_input[3]))
    #nie jestem pewna, czy wsadzanie float ma sens, dlatego rzutuje na inta.
    chars = get_chars_amount(words_list)
    words = get_words_amount(words_list)
    punct = get_punct_amount(words_list)
    letters = get_letters_amount(chars, punct)
    vowels, consonants = get_vowels_consonants_amount(words_list)

    print("Chars : " + str(chars))
    print("Words : " + str(words))
    print("Punct : " + str(punct))
    print("Letters : " + str(letters))
    print("Vowels : " + str(vowels))
    print("Consonants : " + str(consonants))

main()
