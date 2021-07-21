# change html of book

import glob
import subprocess
import re
from typing import ClassVar
# subprocess.run("mkdir -p docs/", shell=True, check=True)
files  = glob.glob("./docs/uniq-*-*-*.txt")
# files = ["README.md"]
# files = ["tmp/0001-private-fields.html"]
d = {}
for file in files:
    raw = ""
    with open(file, 'r') as f:
        raw = f.read()
        lines = raw.split("\n")
        for e in lines:
            e = e.strip()
            # print(e)
            if e == "":
                continue
            val, key = e.split()
            if key not in d.keys():
                d[key] = int(val)
            else:
                d[key] += int(val)
d = sorted(d.items(), key=lambda x:-x[1])
print(d)
csv = ""
hist = ""
for key, val in d:
    csv += "{},\"\"\n".format(key)
    hist += "{}\t{}\n".format(key, val)

with open("dict.csv", 'w') as f:
    f.write(csv)
with open("hist.txt", 'w') as f:
    f.write(hist)