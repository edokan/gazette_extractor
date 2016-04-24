#!/bin/bash

nameOfDir=$(checkNextNumberOfGazette)
function checkNextNumberOfGazette()
{
max=$(ls -1d */ | grep '^gazette[0-9]\+/$' | sed 's/gazette\([0-9]\+\)\//\1/' | sort -n -r | head -n 1);
next=$[max+1];
number=$(printf '%04d' $next);
name="gazette$number";
echo "$name";
}

function makeDir()
{
	mkdir -p $nameOfDir
}
function changeDir(){
	cd nameOfDir
}
function makeOginalDir(){
	mkdir -p "orginal"
}
function makePageDirs(){
	
 
}
function addRectangle(){
	/* wywołanie funkcjji generującej rectangle */
}
function addXml(){
/* djvutoxml  > xml.xml */
}

function makeAllStructure(){
	makeDir
  changeDir
  makeOrginalDir
  makePagesDirs
  addRectangle
  addXml
}
makeAllStructure
