import sys
import pickle
import codecs

if __name__ == "__main__":
    with codecs.open(sys.argv[1], encoding='utf-8') as codes:
        bpe_codes = [tuple(item.split()) for item in codes]

    # some hacking to deal with duplicates (only consider first instance)
    bpe_codes = dict([(code, i) for (i, code) in reversed(list(enumerate(bpe_codes)))])

    with open(sys.argv[2], 'wb') as output:
        pickle.dump(bpe_codes, output)
