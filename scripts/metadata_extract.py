import sys
from collections import OrderedDict
from nltk.tokenize import word_tokenize
import argparse

parser = argparse.ArgumentParser(description = 
        """
        Extract metadata features from DJVU metadata.
        """
        )
parser.add_argument("-y", help = "Default year of newspaper if none is specified", default = "1930", required = False, type = str)
args = parser.parse_args()


metadata = {}
features = OrderedDict()

def get_gazette_title():
    splitted = word_tokenize(metadata["title"], language = "polish")
    tokens = [w for w in splitted if w.isalnum()]
    
    for token in tokens:
        features["INTITLE+" + token] = ""

def get_gazette_year():
    durationStart = metadata.get("durationStart", 0)
    durationEnd = metadata.get("durationEnd", 0)
    if durationStart != 0:
        features["YEAR"] = durationStart[:4]
    elif durationEnd != 0:
        features["YEAR"] = durationEnd[:4]
    else:
        features["YEAR"] = args.y


if __name__ == "__main__":
    for line in sys.stdin:
        name, value = [x.strip().replace('"', '') for x in line.split("\t")]
        metadata[name] = value

    get_gazette_title()
    get_gazette_year()

    for feature in features:
        if features[feature] == "":
            sys.stdout.write(feature + " ")
        else:
            sys.stdout.write(feature + ":" + features[feature] + " ")
        sys.stdout.flush()
