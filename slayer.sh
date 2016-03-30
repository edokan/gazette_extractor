#!/bin/bash
echo "Ohayou"
mkdir -p "foreground"
mkdir -p "background"
f="foreground/"
b="background/"
tiff=".tiff"

for i in $( ls -p  | grep *.djvu); do
	y=$i
	i=${i%.djvu}
	tifffilename=$i$tiff
	d=$b$tifffilename
	u=$f$tifffilename
	ddjvu -mode=background $y $d
	ddjvu -mode=foreground $y $u
done
