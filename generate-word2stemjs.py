import glob
import subprocess

## make dictionary
subprocess.run("mkdir -p docs/", shell=True, check=True)
subprocess.run("bin/tsv2json data/dic.ja.tsv > docs/dic.ja.json", shell=True)
subprocess.run("echo 'var dic = ' > docs/dic.ja.js", shell=True)
subprocess.run("cat docs/dic.ja.json >> docs/dic.ja.js", shell=True)

## generate word2stem.js
files  = glob.glob("./book/*-*-*.html")
# files = ["tmp/0001-private-fields.html"]
for filename in files:
    print("{} start".format(filename))
    uniq_name = filename.split('/')[2].split('.')[0] # name: ./book/0001-private-fields.html
    subprocess.run("bin/s2t {} > docs/rfc-{}.txt".format(filename, uniq_name), shell=True, check=True)
    subprocess.run("bin/tokenizer docs/rfc-{}.txt > docs/tokens-all-{}.txt".format(uniq_name, uniq_name), shell=True, check=True)
    subprocess.run("bin/tokenizer --json docs/rfc-{}.txt > docs/tokens-all-{}.json".format(uniq_name, uniq_name), shell=True, check=True)
    subprocess.run("bin/gospec filter1 < docs/tokens-all-{}.txt > docs/tokens1-{}.txt 2> docs/tokens1-{}.log".format(uniq_name, uniq_name, uniq_name), shell=True)
    subprocess.run("bin/gospec filter2 < docs/tokens1-{}.txt > docs/tokens2-{}.txt 2> docs/tokens2-{}.log".format(uniq_name, uniq_name, uniq_name), shell=True)
    subprocess.run("bin/gospec filter3 < docs/tokens2-{}.txt > docs/tokens3-{}.txt 2> docs/tokens3-{}.log".format(uniq_name, uniq_name, uniq_name), shell=True)
    subprocess.run("bin/gospec filter4 < docs/tokens3-{}.txt > docs/tokens4-{}.txt 2> docs/tokens4-{}.log".format(uniq_name, uniq_name, uniq_name), shell=True)
    subprocess.run("cat docs/tokens4-{}.txt | sort | uniq | tr '[:upper:]' '[:lower:]' > docs/tokens-uniq-{}.txt".format(uniq_name, uniq_name), shell=True)
    subprocess.run("bin/gospec normalize < docs/tokens-uniq-{}.txt > docs/word2stem-{}.txt 2> docs/word2stem-{}.log".format(uniq_name, uniq_name, uniq_name), shell=True)
    subprocess.run("bin/gospec normalizejson < docs/tokens-uniq-{}.txt > docs/word2stem-{}.json 2>/dev/null".format(uniq_name, uniq_name), shell=True)
    subprocess.run("echo 'var word2stem = ' > docs/word2stem-{}.js".format(uniq_name), shell=True)
    subprocess.run("cat docs/word2stem-{}.json >> docs/word2stem-{}.js".format(uniq_name, uniq_name), shell=True)
    subprocess.run("bin/gospec count < docs/tokens4-{}.txt > docs/count-{}.txt 2>/dev/null".format(uniq_name, uniq_name), shell=True)
    subprocess.run("bin/gospec uniq < docs/tokens4-{}.txt > docs/uniq-{}.txt 2>/dev/null".format(uniq_name, uniq_name), shell=True)
