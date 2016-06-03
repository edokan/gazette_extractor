### GAZETTE  ###

SHELL := /bin/bash

.PHONY: all preprocess merge clean

TARGETS=$(shell ls $$PWD/polygon/*.djvu | sed 's|.djvu$$|.features.vw|g')

all: preprocess merge

preprocess: ${TARGETS}

merge: training.vw

clean:
	rm -r $$PWD/polygon/*/
	rm -r $$PWD/polygon/*.features.vw

############################## PREPROCESS #######################################

%.features.vw: %.analyzed
	echo $<
	cat $*/*.features.vw > $@
	
%.analyzed: %.djvu
	sh analyze_pages.sh $< 
	#touch $@


################################### MERGE #######################################

training.vw:
	cat $$PWD/polygon/*.features.vw > training.vw
