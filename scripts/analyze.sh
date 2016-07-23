#!/bin/bash

DDJVU_FILE=$1
FILE_DIR=$(dirname "${DDJVU_FILE}")
DDJVU_NAME=$(basename "${DDJVU_FILE}" .djvu)
PAGES=$(djvused -e n "${DDJVU_FILE}")
DIR=${FILE_DIR}/${DDJVU_NAME}

#Analyze metadata.
python3 metadata_extract.py < $DIR/metadata.tsv > $DIR/metadata.vw

for i in $(seq 1 $PAGES)
do
    #Clean xml of wrong chars
    python xml_cleaner.py $DIR/page_$i.xml > $DIR/page_$i.xml_cleaned

    #Extract word, lines and paragraph coordinates from xml
    python3 xml_extract.py \
        < $DIR/page_$i.xml_cleaned \
        > $DIR/page_$i.xml_coord

    #Extract potential necro rectangles
   python rectangle.py -f $DIR/page_$i.tiff -v \
       < $DIR/page_$i.xml_coord \
       > $DIR/page_$i.rect

   #Extract graphic features
   python graphic_features_extractor.py -f $DIR/page_$i.tiff \
       < $DIR/page_$i.rect \
       > $DIR/page_$i.graphic_features.vw

   #Extract text features
   python3 text_features_extractor.py -pc $DIR/page_$i.rect \
       < $DIR/page_$i.xml_cleaned \
       > $DIR/page_$i.text_features.vw

   #Merge all page's features into one file.

   paste \
       $DIR/page_$i.rect \
       $DIR/page_$i.graphic_features.vw \
       $DIR/page_$i.text_features.vw \
       | \
       sed "s,^,| ${DDJVU_NAME}.djvu\t$(cat $DIR/metadata.vw)\tPAGE:${PAGE}\t,g" \
       > $DIR/page_$i.features.vw

done

#Merge all pages features into one file.
cat $DIR/page_*.features.vw > ${FILE_DIR}/${DDJVU_NAME}.features.vw

#Touch flag to finish things up.
touch ${FILE_DIR}/${DDJVU_NAME}.ANALYZED
