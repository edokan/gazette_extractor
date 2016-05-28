### GAZETTE PREPROCESSING ###

## Works for only 1 page, multiple page in progress ###

all: /home/alvis/Studia/gazette_analyzer/makefile_test/features.vw

.SECONDARY:

### 1. Create preprocessing directory
###	   Extract metadata file

%/preprocessing/metadata.tsv: %/*.djvu
	mkdir -p $(@D)
	djvused -u $< -e 'print-meta' > $@

%/extracted: %/*.djvu
	sh unpack.sh $<

%/analyzed: %/extracted
	

%/features.vw: %/analyzed
	touch $@

