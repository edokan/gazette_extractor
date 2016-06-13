#!/bin/bash

FILE_PATH=$1
DIR=$(dirname "${FILE_PATH}")
DDJVU=$(basename "${FILE_PATH}")
PAGES=$(djvused -e n ${DIR}/${DDJVU})
SPLIT=6


#UNPACKING ALL FILES NEEDED TO PROCEED
sh unpack.sh ${FILE_PATH}

#EXTRACT METADATA
python3 metadata_extraction.py < ${DIR}/processing/metadata.tsv > ${DIR}/processing/metadata.vw
> ${DIR}/features.vw

#ANALYZING EVERY PAGE SEPARATELY
for i in $(seq 1 $PAGES)
do
    echo ${DIR}/processing/page_${i}.tiff

    #GET RECT
    
    ### BASELINE
    python rectangle.baseline.py -f ${DIR}/processing/page_${i}.black.tiff -s ${SPLIT} > ${DIR}/processing/page_${i}.rect

    ### SZUKANIE PROSTOKATOW NA OBRAZKU - CZEKA NA PORZADNY INPUT
    cat ${DIR}/processing/page_${i}.xml | grep 'WORD' | sed 's,<WORD coords=",,g' | sed 's,".*,,g' | sed 's|,| |g' | python rectangle.skeleton.py -f ${DIR}/processing/page_${i}.full.tiff -v > ${DIR}/processing/page_${i}.rect

    #GET GRAPHIC FEATURES OF RECTANGLES
    python graphic_feature_extraction.py -f ${DIR}/processing/page_${i}.black.tiff < ${DIR}/processing/page_${i}.rect > ${DIR}/processing/page_${i}.graphic_features.vw


    #GET TEXT FEATURES OF RECTANGLES
    #to do
    
    python wrong_chars_xml_cleaner.py ${DIR}/processing/page_${i}.xml | python3 text_extractor.py -pc ${DIR}/processing/page_${i}.rect > ${DIR}/processing/page_${i}.text

    #LANGUAGE MODEL OUTPUT
    #to do

    #MERGE ALL FEATURES OF PAGE INTO ONE FILE
    paste ${DIR}/processing/page_${i}.rect ${DIR}/processing/page_${i}.graphic_features.vw ${DIR}/processing/page_${i}.text | sed "s,^,${FILE_PATH}\t$(cat ${DIR}/processing/metadata.vw)\tPAGE:${i}\t,g" >> ${DIR}/features.vw 

done

