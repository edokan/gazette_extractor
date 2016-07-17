#####################################################################################################
#																									#
#										MOTHERSHIP MAKEFILE											#
#																									#
#####################################################################################################

.PHONY: train unpack analyze get-classes merge train-vw

SHELL=/bin/bash

DJVU_LIST=$(wildcard TRAIN/*.djvu)
UNPACKED_LIST=$(patsubst %.djvu,%.UNPACKED,$(DJVU_LIST))
ANALYZED_LIST=$(patsubst %.djvu,%.ANALYZED,$(DJVU_LIST))
CLASSIFIED_LIST=$(patsubst %.djvu,%.CLASSIFIED,$(DJVU_LIST))

train: unpack analyze get-classes merge train-vw

### UNPACK

unpack: $(UNPACKED_LIST)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"

%.UNPACKED: %.djvu
	./unpack.sh $*.djvu

### ANALYZE

analyze: $(ANALYZED_LIST)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"

%.ANALYZED: %.UNPACKED
	./analyze.sh $*.djvu




