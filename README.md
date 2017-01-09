Manual and tutorial : http://gazette-extractor.readthedocs.io/

ENGINEER PROJECT - GAZETTE EXTRACTOR

Authors:

Maximiliana Behnke

Sandra Ambroziak

Summary:


in progress

How to train:

1) make train-split

Split data into separate files for multiprocessing in the future.

2) make train -j X

Train model analyzing X papers at the same time.


How to re-train model (ie. after adding more newspapers):


1) make train-clean

Cleans some files to create them anew.

2) make train-split

3) make train -j X


How to test:


1) make test -j X

Test model analyzing X papers at the same time.


How to remove everything:

- make train-purge
- make test-purge
- make purge = train-purge + test-purge
