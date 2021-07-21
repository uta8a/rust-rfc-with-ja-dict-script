# change html of book

import glob
import re
files  = glob.glob("./book/*-*-*.html")
# files = ["tmp/0001-private-fields.html"]
for file in files:
    filename = file.split("/")[2].split(".")[0] # ./book/0001-private-fields.html
    raw = ""
    with open(file, 'r') as f:
        raw = f.read()
        raw = re.sub('</title>', '</title>\n\t\n\t<!-- BEGIN custom code for dictionary -->\n\t<link type="text/css" rel="stylesheet" href="addon/dictionary.css">\n\t<script src="addon/word2stem/word2stem-{}.js"></script>\n\t<script src="addon/dic.ja.js"></script>\n\t<script src="addon/main.js"></script>\n\t<!-- END custom code for dictionary -->\n'.format(filename), raw)
    with open(file, 'w') as f:
        f.write(raw)