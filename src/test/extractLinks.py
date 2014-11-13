import re

pattern=r"""\([0-9]*,0,(\\[\'\"])(?:\\\\\1|.)*?\1,[0-9]*\)"""
regex = re.compile(pattern)
f = open('enwiki-20141008-pagelinks.sql')
for line in f:
    b = line.encode('string-escape')
    matches = regex.finditer(b, re.DOTALL|re.MULTILINE)
    for match in matches:
        print match.group()
