#!/bin/bash

FILES=$1/*.djvu
TRAIN=$2
TEST=$3

# Calculate MD5sum for every file in catalog.

LIST="0 1 2 3"

for FILE in $FILES
do
    DJVU_FILE=$(basename $FILE)
    NECRO_FILE=$(basename $FILE .djvu).necro
    MD5=$(md5sum $FILE | cut -d " " -f 1)
    LAST_CHAR=$(echo -n $MD5 | tail -c 1)

    if [[ $LIST =~ $LAST_CHAR ]]
    then
        echo "TEST" $DJVU_FILE $NECRO_FILE
        ln -sf $FILE $TEST/$DJVU_FILE
        ln -sf $FILE $TEST/$NECRO_FILE
    else
        echo "TRAIN" $DJVU_FILE $NECRO_FILE
        ln -sf $FILE $TRAIN/$DJVU_FILE
        ln -sf $FILE $TRAIN/$NECRO_FILE
    fi

done
