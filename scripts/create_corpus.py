import sys, argparse, xml.etree.ElementTree as ET

def cut_xml(_x1, _y1, _x2, _y2, tree):
    root = ET.parse(tree)
    words_list = []
    for word in root.iter('WORD'):
        if word.text is not None:
            coordinates = list(word.attrib.values())[0].split(',')
            x1 = coordinates[0]
            y1 = coordinates[1]
            x2 = coordinates[2]
            y2 = coordinates[3]
        if (int(x1) >= int(_x1) and int(x2) <= int(_x2) and int(y1) >= int(_y1) and int(y2) <= int(_y2) and word.text is not None): words_list.append(word.text)
    return " ".join(words_list).lower() + "\n"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extract necrologies text to corpus file.")
    parser.add_argument('-fn', help="necrologue filename where coordinates are kept. -> newspapertitle.necro")
    args = parser.parse_args()

    filename = args.fn
    gazette_title = filename.replace(".necro", "")
    necrologue = dict()

    with open(filename) as necrologues_data:
        for line in necrologues_data:
            for necrologue_data in line.split(" "):
                data = necrologue_data.split("/")
                if len(data) == 2 : 
                    coordinates = data[1]
                    page = data[0]
                    necrologue[coordinates] = page

    for coord, page in necrologue.items():
        coordinates = coord.split(",")
        page_dir = str(gazette_title) + "/page_" + str(page) + ".xml_cleaned"
        page_with_necro = str(gazette_title) + "/page_" + str(page) + ".txt"
        sys.stdout.write(cut_xml(coordinates[0], coordinates[1], coordinates[2], coordinates[3], \
                                 page_dir))
        #Creates corpus of pages with necrologies
        with open(page_with_necro) as page_data:
            for line in page_data:
                with open("LM/corpus_pages.txt", "ab") as corpus_pages:
                    corpus_pages.write(bytes(line.lower(), 'UTF-8'))
