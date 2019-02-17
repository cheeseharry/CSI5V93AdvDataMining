import sys
import networkx as nx
sys.setrecursionlimit(10000000)

BP = set()  # biological_process
MF = set()  # molecular_function
CC = set()  # cellular_component

BP_parent = set()  # BP - BP_parent = BP_Leaf
MF_parent = set()
CC_parent = set()

BP_Leaf_List = []  # BP - BP_parent = BP_Leaf
MF_Leaf_List = []
CC_Leaf_List = []

BP_Root_List = []  # root list
MF_Root_List = []
CC_Root_List = []

term_info_List = []

BP_Graph = nx.DiGraph()
MF_Graph = nx.DiGraph()
CC_Graph = nx.DiGraph()


# Create DAG
# para: term_info_list[]
def create_DAG():
    G = nx.DiGraph()
    for term_info in term_info_List:

        pass
    pass


# find longest shortest path
# para: DAG
def longest_shortest_path(G, root_list, leaf_list):
    shortest_root_leaf_path = []
    for root in root_list:
        for leaf in leaf_list:
            path_len, path = bfs_shortest_path(G, root, leaf)
            shortest_root_leaf_path.append(path_len)
            pass
        pass

    shortest_root_leaf_path = sorted(shortest_root_leaf_path,reverse=True)
    return shortest_root_leaf_path
    pass


# bfs find shortest path
def bfs_shortest_path(G, source, target):
    if source not in G or target not in G:
        msg = 'Either source {} or target {} is not in G'
        raise nx.NodeNotFound(msg.format(source, target))

    # call helper to do the real work
    results = bfs_helper(G, source, target)
    pred, succ, w = results

    # build path from pred+w+succ
    path = []
    # from source to w
    while w is not None:
        path.append(w)
        w = pred[w]
    path.reverse()
    # from w to target
    w = succ[path[-1]]
    while w is not None:
        path.append(w)
        w = succ[w]

    return len(path), path


# Returns (pred, succ, w)
def bfs_helper(G, source, target):
    if target == source:
        return {target: None}, {source: None}, source

    if G.is_directed():
        Gpred = G.pred
        Gsucc = G.succ
    else:
        Gpred = G.adj
        Gsucc = G.adj

    # predecesssor and successors in search
    pred = {source: None}
    succ = {target: None}

    # initialize fringes, start with forward
    forward_fringe = [source]
    reverse_fringe = [target]

    while forward_fringe and reverse_fringe:
        if len(forward_fringe) <= len(reverse_fringe):
            this_level = forward_fringe
            forward_fringe = []
            for v in this_level:
                for w in Gsucc[v]:
                    if w not in pred:
                        forward_fringe.append(w)
                        pred[w] = v
                    if w in succ:  # path found
                        return pred, succ, w
        else:
            this_level = reverse_fringe
            reverse_fringe = []
            for v in this_level:
                for w in Gpred[v]:
                    if w not in succ:
                        succ[w] = v
                        reverse_fringe.append(w)
                    if w in pred:  # found path
                        return pred, succ, w

    raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))


# First Scan
# Construct term
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
    pass


# parent [child,child] list
# para: term_info_list[]
def child_List():
    pass


# add parent-child & parent-set to find root
def add_parent_helper(child_id, parent_id, parent_list, BP_Flag, MF_Flag, CC_Flag, root_mark):
    if parent_id in BP and BP_Flag:  # add parent only when in the same ontology
        parent_list.append(parent_id)
        BP_parent.add(parent_id)

        # construct DAG
        BP_Graph.add_edge(parent_id, child_id)  # parent -> child graph
        root_mark = False

    if parent_id in MF and MF_Flag:  # add parent only when in the same ontology
        parent_list.append(parent_id)
        MF_parent.add(parent_id)

        # construct DAG
        MF_Graph.add_edge(parent_id, child_id)
        root_mark = False

    if parent_id in CC and CC_Flag:  # add parent only when in the same ontology
        parent_list.append(parent_id)
        CC_parent.add(parent_id)

        # construct DAG
        CC_Graph.add_edge(parent_id, child_id)
        root_mark = False
    return root_mark
    pass


# Second Scan
# add parent child relationship
def add_parent_child(term_line):
    child_id = ""
    namespace = ""
    parent_list = []
    child_list = []

    BP_Flag = False  # mark child's Ontology
    MF_Flag = False
    CC_Flag = False

    root_mark = True
    is_BP_root = True  # mark if have no parent -> root
    is_MF_root = True  # mark if have no parent -> root
    is_CC_root = True  # mark if have no parent -> root

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
            root_mark = add_parent_helper(child_id, parent_id, parent_list, BP_Flag, MF_Flag, CC_Flag, root_mark)
            pass

        if line.startswith("relationship: part_of"):
            parent_id = line[22:32]
            root_mark = add_parent_helper(child_id, parent_id, parent_list, BP_Flag, MF_Flag, CC_Flag, root_mark)
            pass

        if line.startswith("is_a:"):
            parent_id = line[6:16]
            root_mark = add_parent_helper(child_id, parent_id, parent_list, BP_Flag, MF_Flag, CC_Flag, root_mark)
            pass

    term_info = {"id": child_id, "namespace": namespace, "parent": parent_list, "child": child_list, "root_mark": root_mark}
    # add root to list
    if root_mark and BP_Flag:
        BP_Root_List.append(child_id)
    if root_mark and MF_Flag:
        MF_Root_List.append(child_id)
    if root_mark and CC_Flag:
        CC_Root_List.append(child_id)

    return term_info


def read_input():
    file = open("go.obo")
    fileStr = file.read()
    termBlock = fileStr.split("[Term]")

    for termStr in termBlock:
        if termStr.__contains__("is_obsolete: true"):  # remove obsolete term
            continue
        term_line = termStr.splitlines()
        construct_term(term_line)
        pass

    for termStr in termBlock:
        if termStr.__contains__("is_obsolete: true"):  # remove obsolete term
            continue
        term_line = termStr.splitlines()
        if term_line:  # remove empty list []
            term_info = add_parent_child(term_line)
            term_info_List.append(term_info)
            pass
        pass
    pass


if __name__ == '__main__':
    read_input()
    #print(term_info_List)
    #print(BP)
    #print(BP_parent)
    print("BP Size: " + str(len(BP)))
    print("MF Size: " + str(len(MF)))
    print("CC Size: " + str(len(CC)))
    #print(BP_Leaf_List)
    print("BP Root: " + str(BP_Root_List))
    print("MF Root: " + str(MF_Root_List))
    print("CC Root: " + str(CC_Root_List))

    BP_Leaf_Set = BP - BP_parent
    BP_Leaf_List = list(BP_Leaf_Set)
    print("BP Leaf Size: " + str(len(BP_Leaf_List)))

    MF_Leaf_Set = MF - MF_parent
    MF_Leaf_List = list(MF_Leaf_Set)
    print("MF Leaf Size: " + str(len(MF_Leaf_List)))

    CC_Leaf_Set = CC - CC_parent
    CC_Leaf_List = list(CC_Leaf_Set)
    print("CC Leaf Size: " + str(len(CC_Leaf_List)))

    #5
    BP_longest_shortest_path_len = longest_shortest_path(BP_Graph,BP_Root_List,BP_Leaf_List)
    print("BP_longest_shortest_path_len: " + str(BP_longest_shortest_path_len[0]))

    MF_longest_shortest_path_len = longest_shortest_path(MF_Graph,MF_Root_List,MF_Leaf_List)
    print("MF_longest_shortest_path_len: " + str(MF_longest_shortest_path_len[0]))

    CC_longest_shortest_path_len = longest_shortest_path(CC_Graph,CC_Root_List,CC_Leaf_List)
    print("CC_longest_shortest_path_len: " + str(CC_longest_shortest_path_len[0]))

    #print(BP_Graph.number_of_edges())

