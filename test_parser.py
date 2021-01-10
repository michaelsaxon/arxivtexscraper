from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode
import pylatexenc
import sys

fname = sys.argv[1]
with open(fname, "r") as f:
    tex = f.read()
    print(fname)
walker = LatexWalker(tex)
nodelist, pos, leen =  walker.get_latex_nodes()
charslist = []
for node in nodelist:
    if node.isNodeType(pylatexenc.latexwalker.LatexEnvironmentNode):
        for subnode in node.nodelist:
            if subnode.isNodeType(pylatexenc.latexwalker.LatexCharsNode):
                charslist.append(str(subnode.chars).strip())
                
fullst = " ".join(charslist).replace("\n"," ")


print(fullst)
