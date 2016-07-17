import sys
from collections import OrderedDict
from nltk.tokenize import word_tokenize


metadata = {}
features = OrderedDict()

def get_gazette_title():
    splitted = word_tokenize(metadata["title"], language = "polish")
    tokens = [w for w in splitted if w.isalnum()]
    
    for token in tokens:
        features["INTITLE+" + token] = ""

def get_gazette_year():
    if metadata["durationStart"] is not None:
        features["YEAR"] = metadata["durationStart"][:4]
    else:
        features["YEAR"] = metadata["durationEnd"][:4]


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
    # sys.stdout.write("\n")
