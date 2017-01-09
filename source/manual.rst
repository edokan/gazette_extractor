Manual
==========================================

======
Input
====== 
- **djvu file** of the newspaper in which user wants to find obituary. 
- **in.tsv file (train)** : in this file are kept – filename of the newspaper and page  number with coordinates where obituaries are placed format: 	newspaper_title.djvu	page_number	left_upper_x1_coordinate	left_upper_y1_coordinate	lower_right_x2_coordinate	lower_right_y2_coordinate -> where separators are tabs
- **in.tsv file (test)** : in this file filename of the newspaper is kept. 

========
Install
========
- **make install** : install all of the requirements
- **make install-doc** : install sphinx

======
Train
======
- **make train-split** : creates .necro files (newspaper_title.necro) which include coordinates of obituary and page which contains that obituary.
- **make train** : trains vowpal wabbit model (launches : train-unpack, train-generate, train-lm, train-vw).
- **make train-unpack** : unpacks newspapers from train directory. Extracts metadata (title, type, language etc),  page in tiff, xml and text layer of page.
- **make train-bpe** : trains BPE model based on txt files of newspapers.
- **make train-generate** : generates rectangles “noticed” on page – potential obituaries.
- **make train-classify** : tags generated rectangles using information stored in necro file.
- **make train-lm** : trains language models – char based 3-gram model of necrologies, BPE based 3-gram model of pages with necrologies
- **make train-analyze** : analyzes newspapers – extracts text and graphic features, counts language model score of page rectangles and language model score of page  with current rectangle.
- **make train-merge** : merges vw files of newspapers into train.in file
- **make train-vw** : trains vw model
- **make train-purge** : removes necro, vw files and train.* from train directory; corpora, arpa and klm files from LM directory, BPE model from **BPE** directory.
- **make train-clean** : removes train.* files from train directory. corpora, arpa, klm files from LM directory, BPE model from *BPE* directory. 

=====
Test
=====
- **make test** : tests trained vw model
- **make test-unpack**: unpacks newspapers from *test-A* directory. Extracts metadata (title, type, language etc),  page in tiff, xml and text layer of page.
- **make test-generate** : generates rectangles of page – potential obituaries.
- **make test-analyze** : analyzes newspapers – extracts text and graphic features, counts language model score of page rectangles and language model score of page  with current rectangle.
- **make test-predict** : predicts obituaries for all newspapers in *test-A* directory.
- **make test-merge** : creates out.tsv file where coordinates of obituaries are kept
- **make test-purge** : removes vw, predict, out.tsv and newspaper_title.out.tsv files from test directory
- **make test-clean** : removes out.tsv and newspaper_title.out.tsv files from test directory

=====
Dev
=====
- **make dev** : tests trained vw model
- **make dev-unpack**: unpacks newspapers from *dev-0* directory. Extracts metadata (title, type, language etc),  page in tiff, xml and text layer of page.
- **make dev-generate** : generates rectangles of page – potential obituaries.
- **make dev-analyze** : analyzes newspapers – extracts text and graphic features, counts language model score of page rectangles and language model score of page  with current rectangle.
- **make dev-predict** : predicts obituaries for all newspapers in *dev-0* directory.
- **make dev-merge** : creates out.tsv file where coordinates of obituaries are kept
- **make dev-purge** : removes vw, predict, out.tsv and newspaper_title.out.tsv files from *dev-0* directory
- **make dev-clean** : removes out.tsv and newspaper_title.out.tsv files from *dev-0* directory

======
Clean
======
- **make clean-unpack** : removes txt files from train directory and files created by unpack command.
- **make clean-generate** : removes files created by generate command
- **make clean-classify** : removes files created by classify command
- **make clean-analyze** : removes files created by analyze command
- **make purge** : removes vw, predict, out.tsv and newspaper_title.out.tsv files from test directory; necro, vw files and train.* from train directory; corpora, arpa and klm files from LM directory, BPE model from *BPE* directory.
- **make clean** : removes out.tsv and newspaper_title.out.tsv files from test directory; train.* files from train directory; corpora, arpa, klm files from LM directory, BPE model from *BPE* directory.

====
Doc
====
- **make -f doc_maker html** : creates automatically generated documentation of python modules
- **make -f doc_maker clean** : removes content of build direory

====
Cut
====
- **make cut-necro** : cuts obituary from the newspaper, bases on merged out.tsv and in.tsv files.merged out.tsv and in.tsv files. in.tsv files.
