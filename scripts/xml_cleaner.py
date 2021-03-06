"""
Removes forbidden chars from xml file. By forbidden chars are understood :
- chars which cause xml parser failing.
- non unicode chars.
"""
BYTE_OFFSETS = True
import sys, re, codecs

if __name__ == "__main__":
	clean_output = ""
	fname = sys.argv[1]

	if BYTE_OFFSETS:
	    text = codecs.open(fname, "rb").read()
	else:
	    text = codecs.open(fname, "rb", "utf8", errors="ignore").read()

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

	with codecs.open(fname) as bad_file:
	    for line in bad_file.readlines():
		line = line.replace("&#10;", "")
		for wrong_char in wrong_chars:
		    if wrong_char in line:
		        line = line.replace(wrong_char, "")
		clean_output += line

	print unicode(clean_output, errors="ignore")
