import sys
import math
import networkx as nx
import numpy as np
from sklearn.metrics import roc_auc_score
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


GOA_info_list = []

Gene_Term_Info_List = []

ground_truth_list = []
sim_res_list = []  #similirity result list for 5 method

sim1_score = []
sim2_score = []
sim3_score = []
sim4_score = []
sim5_score = []
gt_score = []

# Create DAG
# para: term_info_list[]
def create_DAG():
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

    #raise nx.NetworkXNoPath("No path between %s and %s." % (source, target))
    return []



def _bidirectional_pred_succ(G, source, target):
    """Bidirectional shortest path helper.

       Returns (pred, succ, w) where
       pred is a dictionary of predecessors from w to the source, and
       succ is a dictionary of successors from w to the target.
    """
    # does BFS from both source and target and meets in the middle
    if target == source:
        return ({target: None}, {source: None}, source)

    # handle either directed or undirected
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


def has_path(G, source, target):
    try:
        nx.shortest_path(G, source, target)
    except nx.NetworkXNoPath:
        return False
    return True


def edge_base_sim_helper(term1,term2):
    path = 0
    if BP_Graph.has_node(term1) and BP_Graph.has_node(term2):
        if nx.has_path(BP_Graph, term1, term2):
            path = nx.shortest_path_length(BP_Graph,term1,term2)
            if path is None:
                return 0
            return 1/(path+1)
    if MF_Graph.has_node(term1) and MF_Graph.has_node(term2):
        if nx.has_path(MF_Graph, term1, term2):
            path = nx.shortest_path_length(MF_Graph,term1,term2)
            if path is None:
                return 0
            return 1/(path+1)
    else:
        return 0
    pass


def most_common_ancestor(G,term1,term2):
    return nx.lowest_common_ancestor(G,term1,term2)
    pass


def best_matching_average(gene0,gene1,term_list0,term_list1):
    sim_total = 0
    for term0 in term_list0:
        #print(term0)
        for term1 in term_list1:
            sim = edge_base_sim_helper(term0, term1)
            if sim is None:
                sim = 0
            else:
                sim_total += sim
            pass
        pass
    return sim_total / (len(term_list0)*len(term_list1)+1)
    pass


def check_node_exist(G,term_list1, term_list2):
    for term1 in term_list1:
        if not G.has_node(term1):
            return False
            pass
        pass

    for term2 in term_list2:
        if not G.has_node(term2):
            return False
            pass
        pass

    return True
    pass


def find_ancestors(G,node):
    return nx.ancestors(G,node)
    pass


def node_base_sim_helper(term1,term2):
    pass


def node_base_sim(gene0,gene1,term_list0,term_list1):
    pt1 = set()
    pt2 = set()
    for term0 in term_list0:
        if BP_Graph.has_node(term0):
            pt1 = pt1 | nx.ancestors(BP_Graph,term0)
            #print(pt1)
        if MF_Graph.has_node(term0):
            pt1 = pt1 | nx.ancestors(MF_Graph,term0)
            #print(pt1)
        else:
            #print("nope?")
            continue

    for term1 in term_list1:
        if BP_Graph.has_node(term1):
            pt2 = pt2 | find_ancestors(BP_Graph,term1)
            #print(pt2)
        if MF_Graph.has_node(term1):
            pt2 = pt2 | find_ancestors(MF_Graph,term1)
        else:
            #print("nope?")
            continue

    if pt1 is None or pt2 is None:
        return 0
    else:
        return len(pt1 & pt2) / (len(pt1 | pt2) + 1)
    pass


def get_info_content_helper(term1,term2):
    if BP_Graph.has_node(term1) and BP_Graph.has_node(term2):
        return 2*get_lca_info(term1) / (get_lca_info(term1) + get_lca_info(term2)+1)

    if MF_Graph.has_node(term1) and MF_Graph.has_node(term2):
        return 2*get_lca_info(term1) / (get_lca_info(term1) + get_lca_info(term2)+1)
    return 0
    pass


def get_lca_info(term):
    for term_info in term_info_List:
        if term_info.__getitem__("id") == term:
            return len(term_info.__getitem__("info_content"))/(len(Gene_Term_Info_List)+1)
        pass
    return 0
    pass


def info_content_sim(gene0,gene1,term_list0,term_list1):
    for term0 in term_list0:
        for term1 in term_list1:
            if check_node_exist(BP_Graph,term0,term1):
                lca = nx.lowest_common_ancestor(BP_Graph,term0,term1)
            if check_node_exist(MF_Graph,term0,term1):
                lca = nx.lowest_common_ancestor(MF_Graph,term0,term1)
    return (len(term_list0)+len(term_list1)) / (len(Gene_Term_Info_List)+1)
    pass


def integrate_base_sim(gene0,gene1,term_list0,term_list1,va1,va2):
    for term0 in term_list0:
        for term1 in term_list1:
            if check_node_exist(BP_Graph,term0,term1):
                lca = nx.lowest_common_ancestor(BP_Graph,term0,term1)
                if lca is None:
                    return 0
                else:
                    return (va1+va2)/2
            if check_node_exist(MF_Graph,term0,term1):
                lca = nx.lowest_common_ancestor(MF_Graph,term0,term1)
                if lca is None:
                    return 0
                else:
                    return (va1+va2)/2
    return (va1+va2)/2
    pass


def find_ancetor_list(term_list0,term_list1):
    pt1 = set()
    pt2 = set()
    for term0 in term_list0:
        if BP_Graph.has_node(term0):
            pt1 = pt1 | nx.ancestors(BP_Graph,term0)
            #print(pt1)
        if MF_Graph.has_node(term0):
            pt1 = pt1 | nx.ancestors(MF_Graph,term0)
            #print(pt1)
        else:
            #print("nope?")
            continue

    for term1 in term_list1:
        if BP_Graph.has_node(term1):
            pt2 = pt2 | find_ancestors(BP_Graph,term1)
            #print(pt2)
        if MF_Graph.has_node(term1):
            pt2 = pt2 | find_ancestors(MF_Graph,term1)
        else:
            #print("nope?")
            continue
    return pt1,pt2
    pass


def my_method_sim(gene0,gene1,term_list0,term_list1):
    G = nx.Graph()  #
    pt1,pt2 = find_ancetor_list(term_list0,term_list1)
    for term0 in pt1:
        for term1 in pt2:
            edge_weight = edge_base_sim_helper(term0, term1)
            if edge_weight is None:
                edge_weight = 0
                G.add_edge(term0, term1, weight=edge_weight)
            else:
                G.add_edge(term0, term1, weight=edge_weight)
                pass
            pass
        pass

    match_res = nx.max_weight_matching(G, maxcardinality=True, weight='weight')
    #print(match_res)
    total_weight = 0
    for edges in match_res:
        total_weight += (G[edges[0]][edges[1]]['weight'])  # get edge weight value
        pass

    return total_weight / (len(match_res)+1)
    pass


def read_human_protein_complexes():

    pass


def read_ground_truth():
    inputFile = open("human_protein_complexes.txt")
    for line in inputFile.readlines():
        line = line.split()
        ground_truth_list.append(line)

    pass


def get_ground_truth(gene0,gene1,term_list0,term_list1):
    for ground_truth in ground_truth_list:
        if gene0 in ground_truth and gene1 in ground_truth:
            return 1
        pass
    return 0
    pass


def auc_report():
    auc_report = open("auc_score.txt", 'w')
    y_true = np.array(gt_score)
    y_scores1 = np.array(sim1_score)
    y_scores2 = np.array(sim2_score)
    y_scores3 = np.array(sim3_score)
    y_scores4 = np.array(sim4_score)
    y_scores5 = np.array(sim5_score)

    print("AUC1 is ", roc_auc_score(y_true, y_scores1))
    print("AUC2 is ", roc_auc_score(y_true, y_scores2))
    print("AUC3 is ", roc_auc_score(y_true, y_scores3))
    print("AUC4 is ", roc_auc_score(y_true, y_scores4))
    print("AUC5 is ", roc_auc_score(y_true, y_scores5))

    auc_report.write("AUC1 is " + str(roc_auc_score(y_true, y_scores1)))
    auc_report.write("\n")
    auc_report.write("AUC2 is " + str(roc_auc_score(y_true, y_scores2)))
    auc_report.write("\n")
    auc_report.write("AUC3 is " + str(roc_auc_score(y_true, y_scores3)))
    auc_report.write("\n")
    auc_report.write("AUC4 is " + str(roc_auc_score(y_true, y_scores4)))
    auc_report.write("\n")
    auc_report.write("AUC5 is " + str(roc_auc_score(y_true, y_scores5)))
    auc_report.write("\n")
    pass


#lowest_common_ancestor(G, node1, node2, default=None)

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
        #BP_parent.add(parent_id)

        # construct DAG
        BP_Graph.add_edge(parent_id, child_id)  # parent -> child graph
        root_mark = False

    if parent_id in MF and MF_Flag:  # add parent only when in the same ontology
        parent_list.append(parent_id)
        #MF_parent.add(parent_id)

        # construct DAG
        MF_Graph.add_edge(parent_id, child_id)
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


    gene_label_list = []
    for GOA_info in GOA_info_list:
        if child_id == GOA_info.__getitem__("go_term"):
            gene = GOA_info.__getitem__("gene")
            #if gene not in gene_label_list:  ## remove duplicate gene annotation
            gene_label_list.append(gene)

    info_content = math.log2(len(gene_label_list) / (len(Gene_Term_Info_List)+1)+1)

    term_info = {"id": child_id, "namespace": namespace, "parent": parent_list, "child": child_list, "root_mark": root_mark,
                 "gene_label_list": gene_label_list, "info_content": info_content}
    

    #term_info = {"id": child_id, "namespace": namespace, "parent": parent_list, "child": child_list, "root_mark": root_mark}

    # print(term_info)
    # add root to list
    if root_mark and BP_Flag:
        BP_Root_List.append(child_id)
    if root_mark and MF_Flag:
        MF_Root_List.append(child_id)
    return term_info


# NO 3 INITIAL depend on GOA_ANNOTATION2
def read_go_obo():
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


# NO 2 INITIAL
# read input and initialize graph
def read_GOA_human():
    inputFile = open("goa_human.gaf")
    for line in inputFile.readlines():
        line = line.split()
        if line.__contains__("IEA"):
            continue
            pass
        if line.__contains__("NOT"):
            continue
            pass

        gene = line[2]
        go_term = line[3]
        ontology = line[6]  # P C F
        namespace = ""

        add_gene_term_relaton(gene,go_term)

        if ontology == "P":  ## add BP
            namespace = "biological_process"
            GOA_info = {"gene": gene, "go_term": go_term, "namespace": namespace}
            GOA_info_list.append(GOA_info)
            pass
        if ontology == "F":  ## add MF
            namespace = "molecular_function"
            GOA_info = {"gene": gene, "go_term": go_term, "namespace": namespace}
            GOA_info_list.append(GOA_info)
            pass

        pass


def add_gene_term_relaton(gene,go_term):
    for gene_term_info in Gene_Term_Info_List:
        if gene == gene_term_info.__getitem__("gene"):
            if go_term not in gene_term_info.__getitem__("go_term"):
                gene_term_info.__getitem__("go_term").append(go_term)
                return
            pass
    pass


# NO1 INITIAL
def read_biogrid_human_ppi_cin():
    inputFile = open("ppi_small.txt")
    for line in inputFile.readlines():
        line = line.split()
        gene0 = line[0]
        gene1 = line[1]

        gene_term_info = {"gene": gene0, "go_term": []}
        if gene_term_info not in Gene_Term_Info_List:
            Gene_Term_Info_List.append(gene_term_info)

        gene_term_info = {"gene": gene1, "go_term": []}
        if gene_term_info not in Gene_Term_Info_List:
            Gene_Term_Info_List.append(gene_term_info)

    pass


def print_similarity_reprot():
    report = open("sim_result.txt", 'w')

    #inputFile = open("biogrid_human_ppi_cln.txt")
    inputFile = open("ppi_small.txt")
    for line in inputFile.readlines():
        line = line.split()
        gene0 = line[0]
        gene1 = line[1]

        term_list0 = []
        term_list1 = []
        for gene_term_info in Gene_Term_Info_List:
            if gene0 == gene_term_info.__getitem__("gene"):
                term_list0 = gene_term_info.__getitem__("go_term")

            if gene1 == gene_term_info.__getitem__("gene"):
                term_list1 = gene_term_info.__getitem__("go_term")

        sim1 = 0
        sim2 = 0
        sim3 = 0
        sim4 = 0
        sim5 = 0
        gt = 0 #1 for true, 0 for false
        sim1 = best_matching_average(gene0,gene1,term_list0,term_list1)
        sim2 = node_base_sim(gene0,gene1,term_list0,term_list1)
        sim3 = info_content_sim(gene0,gene1,term_list0,term_list1)
        sim4 = integrate_base_sim(gene0,gene1,term_list0,term_list1,sim1,sim2)
        sim5 = my_method_sim(gene0,gene1,term_list0,term_list1)
        gt = get_ground_truth(gene0,gene1,term_list0,term_list1)

        sim1_score.append(sim1)
        sim2_score.append(sim2)
        sim3_score.append(sim3)
        sim4_score.append(sim4)
        sim5_score.append(sim5)
        gt_score.append(gt)

        '''
        sim_res_dict = {"sim1": sim1, "sim2": sim2, "sim3": sim3,
                       "sim4": sim4, "sim5": sim5, "gt": gt}

        sim_res_list.append(sim_res_dict)
        '''
        report.write(gene0 + " " + gene1 + " " + str(sim1) + " " + str(sim2) + " "
                     + str(sim3) + " " + str(sim4) + " " + str(sim5) + " " + str(gt))
        report.write("\n")


    pass


if __name__ == '__main__':
    read_ground_truth()

    read_biogrid_human_ppi_cin()
    read_GOA_human()
    read_go_obo()

    print_similarity_reprot()

    auc_report()

    #print(term_info_List)
    #print(BP)
    #print(BP_parent)
    '''''''''
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
    '''


