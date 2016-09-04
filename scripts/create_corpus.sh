#!/bin/bash

INPUT_DJVU=$1

for gazette_djvu in $INPUT_DJVU; do
    gazette_title=`basename $gazette_djvu .djvu`
    if [ -f dev-0/$gazette_title".necro" ]; then
	python3 scripts/create_corpus.py -fn dev-0/$gazette_title".necro" >> LM/corpus_necrologies.txt
    fi
done

touch LM/LM.CORORA.DONE
