#####################################################################################################
#																									#
#										MOTHERSHIP MAKEFILE											#
#																									#
#####################################################################################################

.PHONY: all clean \
	split-data \
	train split-necro train-unpack train-generate train-classify train-analyze train-merge train-vw

.SECONDARY:

SHELL = /bin/bash

### CONFIGURE ME ###

INPUT_DIR = /home/alvis/Studia/necros

######################################### TARGETS ##################################################

### TRAIN ###

TRAIN_DJVU_LIST = $(shell cat dev-0/in.tsv)
TRAIN_UNPACK_TARGETS = $(patsubst %.djvu,\
								  dev-0/%/flags/UNPACK.DONE,\
								  $(TRAIN_DJVU_LIST))
TRAIN_GENERATE_TARGETS = $(patsubst %.djvu,\
						 			dev-0/%/flags/GENERATE.DONE,\
									$(TRAIN_DJVU_LIST))
TRAIN_CLASSIFY_TARGETS = $(patsubst %.djvu,\
								   dev-0/%/flags/CLASSIFY.DONE,\
								   $(TRAIN_DJVU_LIST))
TRAIN_ANALYZE_TARGETS = $(patsubst %.djvu,\
					  			 dev-0/%/flags/ANALYZE_TRAIN.DONE,\
								 $(TRAIN_DJVU_LIST))
TRAIN_MERGE_TARGETS = dev-0/train.vw
TRAIN_VW_TARGETS = dev-0/train.model

### TEST ###

TEST_DJVU_LIST = $(shell cat test-A/in.tsv)
TEST_UNPACK_TARGETS = $(patsubst %.djvu,\
								  test-A/%/flags/UNPACK.DONE,\
								  $(TEST_DJVU_LIST))
TEST_GENERATE_TARGETS = $(patsubst %.djvu,\
								  test-A/%/flags/GENERATE.DONE,\
								  $(TEST_DJVU_LIST))
TEST_ANALYZE_TARGETS = $(patsubst %.djvu,\
					  			  test-A/%/flags/ANALYZE_TEST.DONE,\
								  $(TEST_DJVU_LIST))
TEST_PREDICT_TARGETS = $(patsubst %.djvu,\
					  			  test-A/%/flags/PREDICT.DONE,\
								  $(TEST_DJVU_LIST))
TEST_EXTRACT_TARGETS = $(patsubst %.djvu,\
					  			  test-A/%/flags/EXTRACT.DONE,\
								  $(TEST_DJVU_LIST))
TEST_MERGE_TARGETS = test-A/test.vw
TEST_VW_TARGETS = test-A/train.predict

######################################### GENERAL ##################################################

all: train test

clean:
	rm -rf dev-0/*/ \
		   dev-0/*.necro \
		   dev-0/*.vw \
		   dev-0/train.vw \
		   dev-0/train.model
	
	rm -rf test-A/*/ \
		   test-A/*.vw \
		   test-A/*.predict \
		   test-A/*.out.tsv \
		   test-A/out.tsv

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

%/flags/CLASSIFY.DONE: split-necro %/flags/GENERATE.DONE
	./scripts/classify.sh $*.djvu
	touch $@

### ANALYZE TRAIN ###

%/flags/ANALYZE_TRAIN.DONE: %/flags/CLASSIFY.DONE
	./scripts/analyze_train.sh $*.djvu
	touch $@

### ANALYZE TEST ###

%/flags/ANALYZE_TEST.DONE: %/flags/GENERATE.DONE
	./scripts/analyze_test.sh $*.djvu
	touch $@

### PREDICT ###

%/flags/PREDICT.DONE: dev-0/train.model %/flags/ANALYZE_TEST.DONE
	vw -d $*.vw -i dev-0/train.model -p $*.predict
	touch $@

### PREDICT ###

%/flags/EXTRACT.DONE: %/flags/PREDICT.DONE
	python3 ./scripts/extract_necro.py -i $*.vw -p $*.predict > $*.out.tsv
	touch $@

######################################### TRAINING #################################################


train: train-vw

### 0. SPLIT NECRO ###

split-necro:
	python3 ./scripts/split_necro.py -i dev-0/in.tsv -e dev-0/expected.tsv -o dev-0

######################
		   
### 1. UNPACK ###

train-unpack: $(TRAIN_UNPACK_TARGETS)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"

#################

### 2. GENERATE RECTANGLES ###

train-generate: train-unpack $(TRAIN_GENERATE_TARGETS)
	@echo "FINISHED GENERATING RECTANGLES FOR ALL NEWSPAPERS"

##############################

### 3. CLASSIFY RECTANGLES ###

train-classify: train-generate $(TRAIN_CLASSIFY_TARGETS)
	@echo "FINISHED CLASSIFYING RECTANGLES FOR ALL NEWSPAPERS"


##############################

### 4. ANALYZE ###

train-analyze: $(TRAIN_ANALYZE_TARGETS)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"


##################

### 5. MERGE ###

train-merge: dev-0/train.in
	@echo "CREATED VOWPAL WABBIT TRAINING FILE"

dev-0/train.in: $(TRAIN_ANALYZE_TARGETS)
	cat dev-0/*.vw > dev-0/train.in

###############

### 6. TRAIN VOWPAL WABBIT ###

train-vw: dev-0/train.model
	@echo "CREATED VOWPAL WABBIT MODEL"

dev-0/train.model: dev-0/train.in
	vw -d $< -c --passes 10 -f $@

####################################################################################################


######################################### TESTING  #################################################


test: test-merge
		  
### 1. UNPACK ###

test-unpack: $(TEST_UNPACK_TARGETS)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"

#################

### 2. GENERATE RECTANGLES ###

test-generate: $(TEST_GENERATE_TARGETS)
	@echo "FINISHED GENERATING RECTANGLES FOR ALL NEWSPAPERS"

##############################

### 3. ANALYZE ###

test-analyze: $(TEST_ANALYZE_TARGETS)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"

##################

### 4. PREDICT  ###

test-predict: $(TEST_PREDICT_TARGETS)
	@echo "FINISHED PREDICTING OBITUARIES FOR ALL NEWSPAPERS"


###################

### 5. EXTRACT ###

test-extract: $(TEST_EXTRACT_TARGETS)
	@echo "FINISHED EXTRACTING OBITUARIES FOR ALL NEWSPAPERS"

##################

### 6. MERGE ###

test-merge: test-A/out.tsv
	@echo "FINISHED TESTING"

test-A/out.tsv: $(TEST_EXTRACT_TARGETS)
	cat test-A/*.out.tsv | python3 ./scripts/merge_necro.py -i test-A/in.tsv > test-A/out.tsv


####################################################################################################
