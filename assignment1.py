import networkx as nx
import re

BP = set()  # biological_process
MF = set()  # molecular_function
CC = set()  # cellular_component
term_info_List = []


# construct term
def construct_term(term_line):
    term_id = ""
    namespace = ""
    parent = []
    child = []
    for line in term_line:
        if line.startswith("id:"):
            term_id = line[4:]
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
            if pt in BP:  # add parent only when in the same ontology
                parent.append(pt)
            pass
        if line.startswith("relationship: part_of"):
            pass

        if line.startswith("is_a:"):
            pass

    term_info = {"id": term_id, "namespace": namespace, "parent": parent, "child": child}
    return term_info
    pass


# add parent child relationship
def add_parent_child(term_line):
    child_id = ""
    namespace = ""
    parent_list = []
    child_list = []
    BP_Flag = False  # mark child's Ontology
    MF_Flag = False
    CC_Flag = False
    for line in term_line:
        if line.startswith("id:"):
            child_id = line[4:]
            pass
        if line.startswith("namespace:"):
            namespace = line[11:]

            if namespace.startswith("biological_process"):
                BP_Flag = True
                pass

            if namespace.startswith("molecular_function"):
                MF_Flag = True
                pass

            if namespace.startswith("cellular_component"):
                CC_Flag = True
                pass

        if line.startswith("intersection_of: part_of"):
            parent_id = line[25:35]
            if parent_id in BP and BP_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            if parent_id in MF and MF_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            if parent_id in CC and CC_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            pass
        if line.startswith("relationship: part_of"):
            parent_id = line[25:]
            if parent_id in BP and BP_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            if parent_id in MF and MF_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            if parent_id in CC and CC_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            pass

        if line.startswith("is_a:"):
            parent_id = line[25:]
            if parent_id in BP and BP_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            if parent_id in MF and MF_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            if parent_id in CC and CC_Flag:  # add parent only when in the same ontology
                parent_list.append(parent_id)
            pass

    term_info = {"id": child_id, "namespace": namespace, "parent": parent_list, "child": child_list}
    return term_info


file = open("small.txt")
fileStr = file.read()
termBlock = fileStr.split("[Term]")

for termStr in termBlock:
    if termStr.__contains__("is_obsolete: true"):  # remove obsolete term
        continue
    term_line = termStr.splitlines()
    construct_term(term_line)
    #construct_term(termStr)
    #print(termStr)
    pass
print(len(termBlock))
temp = ""


