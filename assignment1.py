import networkx as nx
import re

BP = set()  # biological_process
MF = set()  # molecular_function
CC = set()  # cellular_component


# construct term
def construct_term(term_line):
    for line in term_line:
        if line.startswith("id:"):
            print(line)
            term_id = line[4:]
            parent = []
            pass
        if line.startswith("namespace:"):
            namespace = line[11:]

            if namespace.startswith("biological_process"):
                BP.add(term_id)
                pass

            if namespace.startswith("molecular_function"):
                MF.add(term_id)
                pass

            if namespace.startswith("cellular_component"):
                CC.add(term_id)
                pass

        if line.startswith("intersection_of: part_of"):
            pt = line[25:35]
            parent.append(pt)
            pass
        if line.startswith("relationship: part_of"):
            pass

        if line.startswith("is_a:"):
            pass
    pass


file = open("small.txt")
fileStr = file.read()
termBlock = fileStr.split("[Term]")

for termStr in termBlock:
    term_line = termStr.splitlines()
    construct_term(term_line)
    # construct_term(termStr)
    # print(termStr)
    pass
print(len(termBlock))
temp = ""


