#!/bin/bash

DDJVU_FILE=$1
FILE_DIR=$(dirname "${DDJVU_FILE}")
DDJVU_NAME=$(basename "${DDJVU_FILE}" .djvu)
PAGES=$(djvused -e n "${DDJVU_FILE}")
NECRO_FILE=${FILE_DIR}/${DDJVU_NAME}.necro
DIR=${FILE_DIR}/${DDJVU_NAME}

echo "Classyfing rectangles for" ${DDJVU_FILE}

for i in $(seq 1 $PAGES)
do

   #Classify potential necro rectangles
   python scripts/classify_rectangles.py \
       -n $NECRO_FILE \
       -r $DIR/page_$i.rect \
       -i $i \
       > $DIR/page_$i.classes

done

