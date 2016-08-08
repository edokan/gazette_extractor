#####################################################################################################
#																									#
#										MOTHERSHIP MAKEFILE											#
#																									#
#####################################################################################################

.PHONY: all clean \
	split-data \
	train train-unpack train-generate train-classify train-analyze train-merge train-vw

.SECONDARY:

SHELL = /bin/bash

### CONFIGURE ME ###

INPUT_DIR = /home/alvis/Studia/necros

######################################### TARGETS ##################################################

### TRAIN ###

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

### TEST ###

TEST_DJVU_LIST = $(wildcard TEST/*.djvu)
TEST_UNPACK_TARGETS = $(patsubst %.djvu,\
								  %/flags/UNPACK.DONE,\
								  $(TRAIN_DJVU_LIST))
TEST_GENERATE_TARGETS = $(patsubst %.djvu,\
						 			%/flags/GENERATE.DONE,\
									$(TEST_DJVU_LIST))
TEST_CLASSIFY_TARGETS = $(patsubst %.djvu,\
								   %/flags/CLASSIFY.DONE,\
								   $(TEST_DJVU_LIST))
TEST_ANALYZE_TARGETS = $(patsubst %.djvu,\
					  			 %/flags/ANALYZE.DONE,\
								 $(TEST_DJVU_LIST))
TEST_MERGE_TARGETS = TEST/test.vw
TEST_VW_TARGETS = TEST/train.predict

######################################### GENERAL ##################################################

all: split-data train
clean:
	rm -rf TRAIN/*/ \
		   TRAIN/*.vw \
		   TRAIN/train.vw \
		   TRAIN/train.model
	
	rm -rf TEST/*/ \
		   TEST/*.vw \
		   TEST/train.vw \
		   TEST/train.model

split-data:
	./scripts/split_data.sh ${INPUT_DIR} TRAIN TEST


####################################### COMMON RULES ###############################################

### UNPACK ###

%/flags/UNPACK.DONE: %.djvu
	./scripts/unpack.sh $<
	touch $@

### GENERATE ###

%/flags/GENERATE.DONE: %/flags/UNPACK.DONE
	./scripts/generate.sh $*.djvu
	touch $@

### CLASSIFY ###

%/flags/CLASSIFY.DONE: %/flags/GENERATE.DONE
	./scripts/classify.sh $*.djvu
	touch $@

### ANALYZE

%/flags/ANALYZE.DONE: %/flags/CLASSIFY.DONE
	./scripts/analyze.sh $*.djvu
	touch $@


######################################### TRAINING #################################################


train: train-vw
		   

### 1. UNPACK ###

train-unpack: $(TRAIN_UNPACK_TARGETS)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"


#################

### 2. GENERATE RECTANGLES ###

train-generate: $(TRAIN_GENERATE_TARGETS)
	@echo "FINISHED GENERATING RECTANGLES FOR ALL NEWSPAPERS"

##############################

### 3. CLASSIFY RECTANGLES ###

train-classify: $(TRAIN_CLASSIFY_TARGETS)
	@echo "FINISHED CLASSIFYING RECTANGLES FOR ALL NEWSPAPERS"


##############################

### 4. ANALYZE ###

train-analyze: $(TRAIN_ANALYZE_TARGETS)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"


##################

### 5. MERGE ###

train-merge: TRAIN/train.vw
	@echo "CREATED VOWPAL WABBIT TRAINING FILE"

TRAIN/train.vw: $(TRAIN_ANALYZE_TARGETS)
	cat TRAIN/*.vw > TRAIN/train.vw

###############

### 6. TRAIN VOWPAL WABBIT ###

train-vw: TRAIN/train.model
	@echo "CREATED VOWPAL WABBIT MODEL"

TRAIN/train.model: TRAIN/train.vw
	vw -d $< -c --passes 10 -f $@

####################################################################################################


######################################### TESTING  #################################################


test: test-score
		   

### 1. UNPACK ###

test-unpack: $(TEST_UNPACK_TARGETS)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"

#################

### 2. GENERATE RECTANGLES ###

test-generate: $(TEST_GENERATE_TARGETS)
	@echo "FINISHED GENERATING RECTANGLES FOR ALL NEWSPAPERS"

##############################

### 3. CLASSIFY RECTANGLES ###

test-classify: $(TEST_CLASSIFY_TARGETS)
	@echo "FINISHED CLASSIFYING RECTANGLES FOR ALL NEWSPAPERS"

##############################

### 4. ANALYZE ###

test-analyze: $(TEST_ANALYZE_TARGETS)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"

TEST/%/flags/ANALYZE.DONE: TEST/%/flags/CLASSIFY.DONE
	./scripts/analyze.sh TEST/$*.djvu
	touch $@

##################

### 5. MERGE ###

test-merge: TEST/test.vw
	@echo "CREATED VOWPAL WABBIT TRAINING FILE"

TEST/test.vw: $(TEST_ANALYZE_TARGETS)
	cat TEST/*.vw > TEST/test.vw

###############

### 6. POLL VOWPAL WABBIT ###

test-vw: TEST/test.predict
	@echo "FINISHED POLLING VOWPAL WABBIT"

TEST/test.predict: TRAIN/train.model TEST/test.vw
	vw -d TEST/test.vw -i TRAIN/train.model -p $@

test-score: TEST/test.predict TEST/test.vw
	paste TEST/test.predict <(cut -d" " -f 1 TEST/test.vw) | \
		python3 scripts/score.py \
		> TEST/test.result


####################################################################################################
