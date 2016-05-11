#!/bin/bash

FILE_PATH=$1
DIR=$(dirname "${FILE_PATH}")
DDJVU=$(basename "${FILE_PATH}")
PAGES=$(djvused -e n ${DIR}/${DDJVU})

cd $DIR
mkdir -p "processing"

for i in $(seq 1 $PAGES)
do
    echo "Extracting page $i"

    #ddjvu -format=tiff -quality=deflate -mode=color -page=$i ${DDJVU} ./processing/page_$i.full.tiff
    #ddjvu -format=tiff -quality=deflate -mode=black -page=$i ${DDJVU} ./processing/page_$i.black.tiff
    #ddjvu -format=tiff -quality=deflate -mode=foreground -page=$i ${DDJVU} ./processing/page_$i.bg.tiff

    ddjvu -format=tiff -quality=60 -mode=color -page=$i ${DDJVU} ./processing/page_$i.full.tiff
    ddjvu -format=tiff -quality=60 -mode=black -page=$i ${DDJVU} ./processing/page_$i.black.tiff
    ddjvu -format=tiff -quality=60 -mode=foreground -page=$i ${DDJVU} ./processing/page_$i.bg.tiff
    
    djvutoxml --with-anno --with-text --page $i ${DDJVU} ./processing/page_$i.xml
done
