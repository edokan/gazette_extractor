#!/bin/bash

INPUT_DJVU=$@

echo $INPUT_DJVU

for gazette_djvu in $INPUT_DJVU; do
    gazette_title=`basename $gazette_djvu .djvu`
    echo $gazette_djvu
    if [ -f train/$gazette_title".necro" ]; then
	    python3 scripts/create_corpus.py -fn train/$gazette_title".necro" >> LM/corpus_necrologies.txt
    fi
done

touch LM/LM.CORORA.DONE
