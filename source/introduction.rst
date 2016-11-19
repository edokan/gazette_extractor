Gazette Reaper – usage tutorial
==========================================

===========
Preparation
===========
    Firstly, user need to invoke *make install* command. It will install all of the necessary tools needed by Gazette Reaper. 
    After successful installation - preparation of train and test set are needed. Put the newspapers to appropriate catalogs – test to *test-A* directory and train to *train* directory. Newspapers from *train* directory must have *in.tsv* file where its titles and obituaries coordinates are kept. In *test-A* file *in.tsv* must contain only titles of newspapers (without obituaries coordinates).

=====
Train
=====
	To train vowpal wabbit model *make train -j X* command need to be invoked, where X is number of newspapers processed at the same time (train without flag -j means that just one newspaper will be processed at the same time). During runtime newspapers are being unpacked,  rectangles with potential obituaries are being generated and classified, bpe and language models are being trained. After these processes graphic, text and language models features of the newspaper are being created in analyze step. The last step merges all of the .vw files, created in the previous one, into *train.in* file which is input for vowpal wabbit.
	Take a look into manual if you want to gain more information about invoking specific steps of training. It's useful when ones need to re-train model without unpacking all of the newspapers again.

=====
Test
=====
	In this phase trained vowpal wabbit model is being tested. Just like in train point, user need to invoke *make test -j X* command, where X is number of newspapers processed at the same time (test without flag -j means that just one newspaper will be processed at the same time). Steps like unpacking and generating are same for both – test and train step. After that graphic, text and language models features of the newspaper are being created in analyze step. Files created during analyze are taken for prediction step – obituaries are being predicted in the newspapers. 
	Take a look into manual if you want to gain more information about invoking specific steps of testing. It's useful when ones need to re-test model without unpacking all of the newspapers again.

=====
Cut necro
=====
	After testing - *out.tsv* file is created. It contains coordinates of the obituaries found in appropriate newspaper (from *in.tsv*). Command *make cut-necro* merges both of files and cut found obituary from the newspaper. The result can be found in *test-A/obituaries* directory.

=====
Cleaning and purging
=====
	By clean is understood removing *out.tsv files, train files, corpora, arpa and klm files from LM directory, and bpe model. Purging removes also vw files and predict.  
	Take a look into manual if you want to gain more information about invoking specific ways of purging and cleaning. formation about invoking specific ways of purging and cleaning. 

=====
Train flow
=====
.. only:: html

    .. image:: http://imagizer.imageshack.us/a/img924/6269/LE56oI.png

.. only:: pdf
    
    .. image:: TRAINING.jpg
=====
Test flow
=====
.. only:: html 

    .. image:: http://imageshack.com/a/img923/69/GiEjJo.png

.. only:: pdf
    
    .. image:: TESTING.jpg
