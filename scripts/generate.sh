#!/bin/bash

DDJVU_FILE=$1
FILE_DIR=$(dirname "${DDJVU_FILE}")
DDJVU_NAME=$(basename "${DDJVU_FILE}" .djvu)
DIR=${FILE_DIR}/${DDJVU_NAME}
PAGES=$(cat "${DIR}/pages.txt")

echo "Generating rectangles for" ${DDJVU_FILE}

for i in $(seq 1 $PAGES)
do
    echo PAGE ${i}
    #Clean xml of wrong chars
    python scripts/xml_cleaner.py $DIR/page_$i.xml > $DIR/page_$i.xml_cleaned

    #Extract word, lines and paragraph coordinates from xml
    python3 scripts/xml_extract.py \
        < $DIR/page_$i.xml_cleaned \
        > $DIR/page_$i.xml_coord

    #Extract potential necro rectangles
    python scripts/rectangle.py -f $DIR/page_$i.tiff \
       -l 200 -u 2500 \
       < $DIR/page_$i.xml_coord \
       > $DIR/page_$i.rect

done

