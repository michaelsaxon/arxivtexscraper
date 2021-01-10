import os

os.chdir("/mnt/hdd/saxon/article_source")
for fname in os.listdir("."):
    if "\n" in fname:
        fixedn = "".join(fname.split("\n"))
        os.rename(fname,fixedn) 
        print(f"fixed {fixedn}")
