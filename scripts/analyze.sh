#!/bin/bash

DDJVU_FILE=$1
FILE_DIR=$(dirname "${DDJVU_FILE}")
DDJVU_NAME=$(basename "${DDJVU_FILE}" .djvu)
PAGES=$(djvused -e n "${DDJVU_FILE}")
DIR=${FILE_DIR}/${DDJVU_NAME}

#Analyze metadata.
python3 scripts/metadata_extract.py < $DIR/metadata.tsv > $DIR/metadata.vw

for i in $(seq 1 $PAGES)
do

   #Extract graphic features
   python scripts/graphic_features_extractor.py -f $DIR/page_$i.tiff \
       < $DIR/page_$i.rect \
       > $DIR/page_$i.graphic_features.vw

   #Extract text features
   python3 scripts/text_features_extractor.py -pc $DIR/page_$i.rect \
       < $DIR/page_$i.xml_cleaned \
       > $DIR/page_$i.text_features.vw

   #Merge all page's features into one file.

   
   paste $DIR/page_$i.classes \
       <(paste \
           $DIR/page_$i.rect \
           $DIR/page_$i.graphic_features.vw \
           $DIR/page_$i.text_features.vw \
           | \
           sed "s,^,| ${DDJVU_NAME}.djvu\t$(cat $DIR/metadata.vw)\tPAGE:$i\t,g" ) \
           > $DIR/page_$i.train.vw

done

#Merge all pages features into one file.
cat `ls -v $DIR/page_*.train.vw` > ${FILE_DIR}/${DDJVU_NAME}.train.vw
