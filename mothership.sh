#!/bin/bash

FILE_PATH=$1
DIR=$(dirname "${FILE_PATH}")
DDJVU=$(basename "${FILE_PATH}")
PAGES=$(djvused -e n ${DIR}/${DDJVU})
SPLIT=10


#UNPACKING ALL FILES NEEDED TO PROCEED
sh unpack.sh ${FILE_PATH}

#EXTRACT METADATA
python3 metadata_extraction.py < ${DIR}/processing/metadata.tsv > ${DIR}/processing/metadata.vw

#ANALYZING EVERY PAGE SEPARATELY
for i in $(seq 1 $PAGES)
do
    echo ${DIR}/processing/page_${i}.tiff

    #GET RECT
    python rectangle.py -f ${DIR}/processing/page_${i}.black.tiff -s ${SPLIT} > ${DIR}/processing/page_${i}.rect

    #GET GRAPHIC FEATURES OF RECTANGLES
    python graphic_feature_extraction.py -f ${DIR}/processing/page_${i}.black.tiff < ${DIR}/processing/page_${i}.rect > ${DIR}/processing/page_${i}.graphic_features.vw


    #GET TEXT FEATURES OF RECTANGLES
    #to do

    #LANGUAGE MODEL OUTPUT
    #to do

    #MERGE ALL FEATURES OF PAGE INTO ONE FILE
    #to do
done

