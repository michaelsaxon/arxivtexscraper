import os
import time
import magic
import requests
import tarfile
import io
import random

with open("checked_ids.txt", "r") as f:
    checked_ids = f.readlines()

checked_ids.sort(key=lambda x: float(x.strip()))

with open("csids.txt", "r") as f:
    ids = f.readlines()

def b_from_a(a, b):
    bidx = 0
    outlist = []
    for aidx, aelem in enumerate(a):
        if bidx < len(b):
            if aelem == b[bidx]:
                #print(f"{aelem},{b[bidx]}")
                bidx += 1
            else:
                outlist.append(aelem)
        else:
            outlist.append(aelem)
    return outlist

ids = list(filter(lambda x: x[0] == "0" or x[0] == "1" or x[0] == "2", ids))

ids = b_from_a(ids, checked_ids)

random.Random(25).shuffle(ids)

num = len(ids)

geturl = lambda idl: "https://export.arxiv.org/e-print/" + idl.strip()

urls = map(geturl, ids)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

prevtime = time.time()

for i, uid in enumerate(ids):
    url = geturl(uid)
    # check if in folderk
    print(f"{i}/{num}: {url}")
    #os.system("wget -P /mnt/hdd/saxon/article_source -H " + url + " >>log.txt 2>&1")
    r = requests.get(url)
    copy_r = r
    styp = magic.from_buffer(r.content, mime=True)
    if styp == 'application/gzip':
        # we can unzip
        try:
            tfl = tarfile.open(fileobj = io.BytesIO(r.content))
            members = tfl.getmembers()
            for member in members:
                if member.name[-4:] == ".tex":
                    # save this file
                    f = tfl.extractfile(member)
                    lines = f.read()
                    with open(f"/mnt/hdd/saxon/article_source/{uid.strip()}_{member.name}", "wb") as of:
                        of.write(lines)
        except:
            print(f"FAILED TO OPEN ARCHIVE {uid}")
    delta = time.time() - prevtime
    prevtime = time.time()
    if delta < 0.2:
        time.sleep(delta)
    if i % 4 == 0:
        time.sleep(0.6)
    with open("/mnt/hdd/saxon/checked_ids.txt","a") as f:
        f.write(uid.strip() + "\n")
