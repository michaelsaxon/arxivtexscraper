import json

with open("arxiv-metadata-oai-snapshot.json","r") as f:
    lines = f.readlines()

for line in lines:
    line = json.loads(line)
    if "categories" in line.keys():
        if "cs." in line["categories"]:
            print(line["id"])


