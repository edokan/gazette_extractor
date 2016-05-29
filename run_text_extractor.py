#!/bin/sh
#Czyszczenie xml, WAŻNE
python bad_xml.py $1
name_unclean=$1
name=$(echo $name_unclean | cut -f 1 -d '.')
clean="_clean.xml"
echo "Created $name$clean"
#Wyrzucanie cech tekstowych
python text_extractor.py $name$clean
