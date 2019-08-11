
from codecs import open
import json
langs = {}
with open("languages.txt","r", "utf-8") as lang_file:
    for elem in [lang.split("\t") for lang in lang_file.readlines()]:
        langs[elem[-1][:-1].strip()] = elem[1]

print(langs)


with open("languages.json",'w') as json_file:
    json.dump(langs, json_file)
