####################################################################################################
#																									#
#										MOTHERSHIP MAKEFILE											#
#																									#
#####################################################################################################

.PHONY: all clean \
	split-data \
	clean purge train-clean train-purge test-clean test-purge \
	train train-split train-unpack train-generate train-classify train-lm train-analyze train-merge train-vw \
	test test-unpack test-generate test-analyze test-predict test-merge \
	dev dev-unpack dev-generate dev-analyze dev-predict dev-merge

.SECONDARY:

SHELL = /bin/bash

### CONFIGURE ME ###

KENLM_BIN = ~/kenlm/build/bin
VOWPAL_WABBIT_DIR = ~/vowpal_wabbit/vowpalwabbit

### INSTALL ###

install-doc:
	sudo apt-get install python-sphinx
	pip install sphinxcontrib-napoleon --user
	pip install rst2pdf

install:
	## TODO Tutaj bedzie instalacja wszystkich paczek i bibliotek.
	sudo apt-get install python-opencv
	pip install https://github.com/kpu/kenlm/archive/master.zip
	sudo pip install -U nltk

	@echo "Finished installing!"

######################################### TARGETS ##################################################

### TRAIN ###

TRAIN_DJVU_LIST = $(shell cat train/in.tsv | cut -f1)
TRAIN_SPLIT_TARGETS = $(patsubst %.djvu,\
								  train/%.necro,\
								  $(TRAIN_DJVU_LIST))
TRAIN_UNPACK_TARGETS = $(patsubst %.djvu,\
								  train/%/flags/UNPACK.DONE,\
								  $(TRAIN_DJVU_LIST))
TRAIN_GENERATE_TARGETS = $(patsubst %.djvu,\
						 			train/%/flags/GENERATE.DONE,\
									$(TRAIN_DJVU_LIST))
TRAIN_CLASSIFY_TARGETS = $(patsubst %.djvu,\
								   train/%/flags/CLASSIFY.DONE,\
								   $(TRAIN_DJVU_LIST))
TRAIN_ANALYZE_TARGETS = $(patsubst %.djvu,\
					  			 train/%/flags/ANALYZE_TRAIN.DONE,\
								 $(TRAIN_DJVU_LIST))
TRAIN_MERGE_TARGETS = train/train.vw
TRAIN_VW_TARGETS = train/train.model

### DEV ###

DEV_DJVU_LIST = $(shell cat dev-0/in.tsv)
DEV_UNPACK_TARGETS= $(patsubst %.djvu,\
								  dev-0/%/flags/UNPACK.DONE,\
								  $(DEV_DJVU_LIST))
DEV_GENERATE_TARGETS = $(patsubst %.djvu,\
								  dev-0/%/flags/GENERATE.DONE,\
								  $(DEV_DJVU_LIST))
DEV_ANALYZE_TARGETS = $(patsubst %.djvu,\
					  			  dev-0/%/flags/ANALYZE_TEST.DONE,\
								  $(DEV_DJVU_LIST))
DEV_PREDICT_TARGETS = $(patsubst %.djvu,\
					  			  dev-0/%/flags/PREDICT.DONE,\
								  $(DEV_DJVU_LIST))
DEV_EXTRACT_TARGETS = $(patsubst %.djvu,\
					  			  dev-0/%/flags/EXTRACT.DONE,\
								  $(DEV_DJVU_LIST))
DEV_MERGE_TARGETS = dev-0/test.vw
DEV_VW_TARGETS = dev-0/train.predict

### TEST ###

TEST_DJVU_LIST = $(shell cat test-A/in.tsv)
TEST_UNPACK_TARGETS= $(patsubst %.djvu,\
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


train-purge:
	rm -rf train/*/ \
		   train/*.necro \
		   train/*.vw \
		   train/train.* \
		   LM/*.txt \
		   LM/necrologies_lm.* \
		   LM/*.DONE \
		   BPE/*

train-clean:
	rm -rf train/train.*
	rm -rf LM/*.txt \
		LM/necrologies_lm.* \
		LM/*.DONE \
		BPE/*

test-purge:
	rm -rf test-A/*/ \
		   test-A/*.vw \
		   test-A/*.predict \
		   test-A/*.out.tsv \
		   test-A/out.tsv
test-clean:
	rm -rf test-A/*.out.tsv \
		   test-A/out.tsv

dev-purge:
	rm -rf dev-0/*/ \
		   dev-0/*.vw \
		   dev-0/*.predict \
		   dev-0/*.out.tsv \
		   dev-0/out.tsv
dev-clean:
	rm -rf dev-0/*.out.tsv \
		   dev-0/out.tsv

clean-unpack:
	rm -rf $(TRAIN_UNPACK_TARGETS)
	rm -f train/*.txt

clean-generate:
	rm -rf $(TRAIN_GENERATE_TARGETS)

clean-classify:
	rm -rf $(TRAIN_CLASSIFY_TARGETS)

clean-analyze:
	rm -rf $(TRAIN_ANALYZE_TARGETS)

purge: train-purge test-purge

clean: train-clean test-clean

#split-data:
	#./scripts/split_data.sh ${INPUT_DIR} TRAIN TEST


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

%/flags/CLASSIFY.DONE: %.necro %/flags/GENERATE.DONE
	./scripts/classify.sh $*.djvu
	touch $@

## TRAIN BPE ###


BPE/corpora.txt: $(TRAIN_UNPACK_TARGETS)
	mkdir -p $(@D)
	cat ./train/*.txt | iconv -f utf-8 -t utf-8 -c \
					  | perl -nle 'print lc' \
					  > ./BPE/corpora.txt


BPE/bpe.model: BPE/corpora.txt
	mkdir -p $(@D)
	cat $< | ./scripts/subword-nmt/learn_bpe.py -v \
					  > $@

BPE/bpe.bin: BPE/bpe.model
	python ./scripts/subword-nmt/binarize_bpe.py $^ $@

### CREATE LM OBITUARY CORPUS ###


LM/LM.CORPORA.DONE: $(TRAIN_GENERATE_TARGETS)
	mkdir -p $(@D)
	./scripts/create_corpus.sh "$(TRAIN_DJVU_LIST)"
	touch $@

### CREATE .ARPA ###
 
LM/LM.ARPA.DONE: BPE/bpe.bin LM/LM.CORPORA.DONE
	cat LM/corpus_necrologies.txt | sed 's/./& /g' | $(KENLM_BIN)/lmplz -S 1G --discount_fallback -o 3 > LM/necrologies_lm.arpa
	cat LM/corpus_pages.txt | ./scripts/subword-nmt/apply_bpe.py --codes $< \
								  | $(KENLM_BIN)/lmplz -S 1G --discount_fallback -o 3 \
								  > LM/pages_lm.arpa
	touch $@

### CREATE BINARY ###
 
LM/LM.BINARY.DONE: LM/LM.ARPA.DONE
	$(KENLM_BIN)/build_binary -s LM/necrologies_lm.arpa LM/necrologies_lm.klm
	$(KENLM_BIN)/build_binary -s LM/pages_lm.arpa LM/pages_lm.klm
	touch $@


### ANALYZE TRAIN ###

%/flags/ANALYZE_TRAIN.DONE: LM/LM.BINARY.DONE %/flags/CLASSIFY.DONE
	./scripts/analyze_train.sh $*.djvu
	touch $@

### ANALYZE TEST ###

%/flags/ANALYZE_TEST.DONE: %/flags/GENERATE.DONE LM/LM.BINARY.DONE BPE/bpe.bin
	./scripts/analyze_test.sh $*.djvu
	touch $@

### PREDICT ###

%/flags/PREDICT.DONE: train/train.model %/flags/ANALYZE_TEST.DONE
	$(VOWPAL_WABBIT_DIR)/vw -d $*.vw -i train/train.model -p $*.predict
	touch $@

### EXTRACT ###

%/flags/EXTRACT.DONE: %/flags/PREDICT.DONE
	python3 ./scripts/extract_necro.py -i $*.vw -p $*.predict > $*.out.tsv
	touch $@

######################################### TRAINING #################################################


train: train-unpack train-generate train-lm train-vw

### 0. SPLIT NECRO ###

train-split:
	python3 ./scripts/split_necro.py -i train/in.tsv -o train

######################
		   
### 1. UNPACK ###

train-unpack: $(TRAIN_UNPACK_TARGETS)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"

#################

### 2. TRAIN BPE ###

train-bpe: BPE/bpe.bin

### 2. GENERATE RECTANGLES ###

train-generate: train-unpack $(TRAIN_GENERATE_TARGETS)
	@echo "FINISHED GENERATING RECTANGLES FOR ALL NEWSPAPERS"

##############################

### 3. CLASSIFY RECTANGLES ###

train-classify: train-generate $(TRAIN_CLASSIFY_TARGETS)
	@echo "FINISHED CLASSIFYING RECTANGLES FOR ALL NEWSPAPERS"


##############################

### 4. TRAIN LM ###                                                                                                                                   
train-lm: LM/LM.BINARY.DONE
	@echo "TRAINED LM"

### 5. ANALYZE ###

train-analyze: $(TRAIN_ANALYZE_TARGETS)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"


##################

### 6. MERGE ###

train-merge: train/train.in
	@echo "CREATED VOWPAL WABBIT TRAINING FILE"

train/train.in: $(TRAIN_ANALYZE_TARGETS)
	cat train/*.vw > train/train.in

###############

### 7. TRAIN VOWPAL WABBIT ###

train-vw: train/train.model
	@echo "CREATED VOWPAL WABBIT MODEL"

train/train.model: train/train.in
	$(VOWPAL_WABBIT_DIR)/vw -d $< -c -k --passes 10 --ngram 4 -b 24 -f $@

####################################################################################################

######################################### DEV  #################################################


dev: dev-merge
		  
### 1. UNPACK ###

dev-unpack: $(DEV_UNPACK_TARGETS)
	@echo "FINISHED UNPACKING ALL NEWSPAPERS"

#################

### 2. GENERATE RECTANGLES ###

dev-generate: $(DEV_GENERATE_TARGETS)
	@echo "FINISHED GENERATING RECTANGLES FOR ALL NEWSPAPERS"

##############################

### 3. ANALYZE ###

dev-analyze: $(DEV_ANALYZE_TARGETS)
	@echo "FINISHED ANALYZING ALL NEWSPAPERS"

##################

### 4. PREDICT  ###

dev-predict: $(DEV_PREDICT_TARGETS)
	@echo "FINISHED PREDICTING OBITUARIES FOR ALL NEWSPAPERS"


###################

### 5. EXTRACT ###

dev-extract: $(DEV_EXTRACT_TARGETS)
	@echo "FINISHED EXTRACTING OBITUARIES FOR ALL NEWSPAPERS"

##################

### 6. MERGE ###

dev-merge: dev-0/out.tsv
	@echo "FINISHED DEVING"

dev-0/out.tsv: $(DEV_EXTRACT_TARGETS)
	cat dev-0/*.out.tsv | python3 ./scripts/merge_necro.py -i dev-0/in.tsv > dev-0/out.tsv

##################


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

##################

### 1. CUT-NECRO

test-cut: test-A/in.tsv test-A/out.tsv
	paste -d" " test-A/in.tsv test-A/out.tsv > test-A/result.tsv
	python ./scripts/cut_necro.py -res test-A/result.tsv

dev-cut: dev-0/in.tsv dev-0/out.tsv
	paste -d" " dev-0/in.tsv dev-0/out.tsv > dev-0/result.tsv
	python ./scripts/cut_necro.py -res dev-0/result.tsv

####################################################################################################
