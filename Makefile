#####################################################################################################
#																									#
#										MOTHERSHIP MAKEFILE											#
#																									#
#####################################################################################################

.PHONY: all split-data train clean unpack generate classify analyze merge train-vw

SHELL = /bin/bash

### CONFIGURE ME ###

INPUT_DIR = ~/Nekrologi/ALL

####################

all: split-data train

split-data:
	./scripts/split_data.sh ${INPUT_DIR} TRAIN TEST

######################################### TRAINING #################################################

TRAIN_DJVU_LIST = $(wildcard TRAIN/*.djvu)
TRAIN_UNPACK_TARGETS = $(patsubst %.djvu,\
								  %/flags/UNPACK.DONE,\
								  $(TRAIN_DJVU_LIST))
TRAIN_GENERATE_TARGETS = $(patsubst %.djvu,\
						 			%/flags/GENERATE.DONE,\
									$(TRAIN_DJVU_LIST))
TRAIN_CLASSIFY_TARGETS = $(patsubst %.djvu,\
								   %/flags/CLASSIFY.DONE,\
								   $(TRAIN_DJVU_LIST))
TRAIN_ANALYZE_TARGETS = $(patsubst %.djvu,\
					  			 %/flags/ANALYZE.DONE,\
								 $(TRAIN_DJVU_LIST))
TRAIN_MERGE_TARGETS = TRAIN/train.vw
TRAIN_VW_TARGETS = TRAIN/train.model

train: unpack generate classify analyze merge train-vw
clean:
	rm -rf TRAIN/*/ \
		   TRAIN/*.train.vw \
		   TRAIN/train.vw \
		   TRAIN/train.model
		   

### 1. UNPACK ###

unpack: $(TRAIN_UNPACK_TARGETS)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"

TRAIN/%/flags/UNPACK.DONE: TRAIN/%.djvu
	./scripts/unpack.sh $<
	touch $@

################

### 2. GENERATE RECTANGLES ###

generate: $(TRAIN_GENERATE_TARGETS)
	@echo "FINISHED GENERATING RECTANGLES FOR ALL NEWSPAPERS"

TRAIN/%/flags/GENERATE.DONE: TRAIN/%/flags/UNPACK.DONE
	./scripts/generate.sh TRAIN/$*.djvu
	touch $@

##############################

### 3. CLASSIFY RECTANGLES ###

classify: $(TRAIN_CLASSIFY_TARGETS)
	@echo "FINISHED CLASSIFYING RECTANGLES FOR ALL NEWSPAPERS"

TRAIN/%/flags/CLASSIFY.DONE: TRAIN/%/flags/GENERATE.DONE
	./scripts/classify.sh TRAIN/$*.djvu
	touch $@

##############################

### 4. ANALYZE ###

analyze: $(TRAIN_ANALYZE_TARGETS)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"

TRAIN/%/flags/ANALYZE.DONE: TRAIN/%/flags/CLASSIFY.DONE
	./scripts/analyze.sh TRAIN/$*.djvu
	touch $@

##################

### 5. MERGE ###

merge: TRAIN/train.vw
	@echo "CREATED VOWPAL WABBIT TRAINING FILE"

TRAIN/train.vw: $(TRAIN_ANALYZE_TARGETS)
	cat TRAIN/*.train.vw > TRAIN/train.vw

###############

### 6. TRAIN VOWPAL WABBIT ###

train-vw: TRAIN/train.model
	@echo "CREATED VOWPAL WABBIT MODEL"

TRAIN/train.model: TRAIN/train.vw
	# Here will be vowpal wabbit command to train model.
	touch $@	

####################################################################################################
