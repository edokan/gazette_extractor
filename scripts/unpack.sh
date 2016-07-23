#!/bin/bash

DDJVU_FILE=$1
FILE_DIR=$(dirname "${DDJVU_FILE}")
DDJVU_NAME=$(basename "${DDJVU_FILE}" .djvu)
PAGES=$(djvused -e n "${DDJVU_FILE}")
DIR=${FILE_DIR}/${DDJVU_NAME}

mkdir -p ${DIR}/flags

echo "Unpacking" ${DDJVU_FILE} - PAGES ${PAGES}

# Extracting metadata.
djvused -u ${DDJVU_FILE} -e 'print-meta' > ${DIR}/metadata.tsv

for i in $(seq 1 $PAGES)
do
    #Extracting page in tiff.
    ddjvu -format=tiff -quality=60 -mode=color -page=$i ${DDJVU_FILE} ${DIR}/page_$i.tiff

    #Extracting page xml.
    djvutoxml --with-anno --with-text --page $i ${DDJVU_FILE} ${DIR}/page_$i.xml
done

