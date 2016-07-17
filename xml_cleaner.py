BYTE_OFFSETS = True
import sys, re, codecs

clean_output = ""
fname = sys.argv[1]

if BYTE_OFFSETS:
    text = open(fname, "rb").read()
else:
    text = codecs.open(fname, "rb", "utf8").read()

wrong_chars = []
rx = re.compile("&#([0-9]+);|&#x([0-9a-fA-F]+);")
endpos = len(text)
pos = 0

while pos < endpos:
    m = rx.search(text, pos)
    if not m: break
    mstart, mend = m.span()
    target = m.group(1)
    if target:
        num = int(target)
    else:
        num = int(m.group(2), 16)
    if not(num in (0x9, 0xA, 0xD) or 0x20 <= num <= 0xD7FF
    or 0xE000 <= num <= 0xFFFD or 0x10000 <= num <= 0x10FFFF):
        wrong_chars.append(m.group())
    pos = mend

with open(fname) as bad_file:
    for line in bad_file.readlines():
        for wrong_char in wrong_chars:
            if wrong_char in line:
                line = line.replace(wrong_char, "")
        clean_output += line

print clean_output
