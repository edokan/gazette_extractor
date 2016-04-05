#!/bin/bash
echo "Ohayou"
s="/"
f="foreground"
b="background"
xml=".xml"
tiff=".tiff"
zero=0
j=0

for i in $( ls *.djvu); do
	j=`expr $j + 1`
	length=$j
	if [ $j -lt 10 ]
	then
	j=$zero$zero$j
	fi
	if [ $j -lt 100 ] && [ $j -gt 9 ]
	then
	j=$zero$j
	fi
	mkdir -p $j
	d=$j$s
	y=$i
	cp $i $j
	i=${i%.djvu}
	xmlfilename=$i$xml
	tifffilenameb=$b$tiff
	db=$d$tifffilenameb
	tifffilenamef=$f$tiff
	df=$d$tifffilenamef
	dx=$d$xmlfilename
	
	ddjvu -format=tiff -quality=deflate -mode=background $y $db
	ddjvu -format=tiff -quality=deflate -mode=foreground $y $df
	djvutoxml $y > $dx
	
done

