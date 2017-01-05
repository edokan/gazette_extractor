import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""
            Extracts found obituaries using VW input file and VW predictions.
            Parses it into Gonito format.
            """
                                     )
    parser.add_argument("-i", help="VW input file", required=True)
    parser.add_argument("-p", help="VW predictions", required=True)
    args = parser.parse_args()

necrologies = []


def extract_necro():
    with open(args.i) as input_file, open(args.p) as predict_file:
        for input_line, predict_line in zip(input_file, predict_file):
            if float(predict_line.strip()) > 0:
                parse_vector(input_line.strip())


def parse_vector(line):
    features = [s for s in line.split() if ":" in s]
    d = {}
    for x in features:
        name, value = x.split(":")
        d[name] = value

    coords = ",".join([d["X1"], d["Y1"], d["X2"], d["Y2"]])
    out = d["PAGE"] + "/" + coords

    necrologies.append(out)

if __name__ == "__main__":
    extract_necro()
    djvu = args.i.split("/")[-1].strip(".vw") + ".djvu"
    necro_string = " ".join(necrologies)
    if necro_string.strip() == "":
        necro_string = "NULL"
    print(djvu + "\t" + necro_string)
