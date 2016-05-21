import sys

metadata = {}

if __name__ == "__main__":
    for line in sys.stdin:
        name, value = [x.strip().replace('"', '') for x in line.split("\t")]
        metadata[name] = value

    if metadata["durationStart"] is not None:
        YEAR_meta = "YEAR:" + metadata["durationStart"][:4]
    else:
        YEAR_meta = "YEAR:" + metadata["durationEnd"][:4]

    TITLE_meta = "_".join(metadata["title"].split(",")[0].split())

    print(TITLE_meta, YEAR_meta, sep = "\t")
