ENGINEER PROJECT - GAZETTE EXTRACTOR

Authors:
Maximiliana Behnke
Sandra Ambroziak

Summary:

in progress

Scripts:

a) Makefile - mothership script. It runs everything!
b) unpack.sh - unpacks djvu file (metadata, tiff, xml)
c) analyze.sh - script that analyzes a newspaper, uses:
    - metadata_extract.py - extracts vector info from djvu metadata
    - xml_cleaner.py - cleans xml from faulty chars
    - xml_extract.py - extracts word, line and paragraph coordinates from xml
    - rectangle.py - creates potential necro rectangles
    - graphic_features_extractor.py - extracts graphic features from generated rectangles
    - text_features_extractor.py - extracts text features from generated rectangles
    - detect_peaks.py - used in graphic_features_extractor.py (imported)
