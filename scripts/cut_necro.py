#!/usr/bin/python3                                                                                                                                   
# -*- coding: utf-8 -*-
"""
Script which creates a folder with found obituaries in the gazette.
"""
import sys
import os
import cv2
import argparse

def read_necrologue_data(result):
    """
    Reads from merged test_dir/in.tsv test_dir/out.tsv necrologue data such as:
    -Newspaper title
    -Coordinates of necrologue
    -Page with necrologue
    """
    with open(result, 'r') as result_necro:
        for line in result_necro.readlines():
            necro_data = line.strip().split(" ")
            title = necro_data[0]
            for necrologue_data in necro_data[1:]:
                data = necrologue_data.split("/")
                coordinates = data[1]
                page = data[0]
                necrologue[coordinates] = [title, page]
    return necrologue

def cut_necrologies(necrologue, obituary_dir, test_dir, show):
    """                                                                                                                                           
    Cut (guessed) necrology from page.
                                                                                                                                                      
    Args:                                                                                                                                         
        necrologue (dict): Dictionary with coordinates of potential necrology.
        obituary_dir (str): Directory where necrologies are kept.
        test_dir (str): Directory of tests
        show (bool): Option to set if we want to see necrologies during script running.
    """
    for key, val in necrologue.items():
        gazette_title = val[0].replace(".djvu","")
        page_with_necro = val[1]
        coordinates = key.split(",")
        path_to_page = test_dir + "/" + gazette_title + "/page_" + page_with_necro + ".tiff"

        page = cv2.imread(path_to_page)
        necro = page[int(coordinates[1]):int(coordinates[3]), int(coordinates[0]):int(coordinates[2])]
        cv2.imwrite(obituary_dir + gazette_title + "_obituary_page_" + page_with_necro + "_" + coordinates[0] + "_" + coordinates[1] + ".tiff", necro)

        if show == True:
            cv2.imshow("necro", necro)
            cv2.waitKey(0)

  
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extractor of guessed necrologies")
    parser.add_argument('-directory', help="directory where test results are kept test-A or dev-0")
    parser.add_argument('-res', help="filename where necrologies data are kept -> directory_name/result.tsv.")
    parser.add_argument('-show', help="set flag as true if you want to see necrologies during running the script", default=False) 
    args = parser.parse_args()

    necrologue = dict()    
    obituary_folder = args.directory + "/obituaries/"

    if not os.path.isdir(obituary_folder):
        os.makedirs(obituary_folder)

    necrologue = read_necrologue_data(args.directory + "/" + args.res)
    cut_necrologies(necrologue, obituary_folder, args.directory, args.show)
