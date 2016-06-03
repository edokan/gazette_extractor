#!/bin/bash

set -e

FILE_PATH=$1
DIR=$(dirname $FILE_PATH)
DJVU_NAME=$(basename $FILE_PATH .djvu)
PAGES=$(djvused -e n $FILE_PATH)

mkdir -p $DIR/$DJVU_NAME

for PAGE in $(seq 1 $PAGES)
do
    echo "Analyzing page ${PAGE}"
    make -f Makefile.page DJVU=${FILE_PATH} PAGE=${PAGE}
done
