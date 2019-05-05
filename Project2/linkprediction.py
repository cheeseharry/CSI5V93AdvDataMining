import networkx as nx

sum1 = 0
sum2 = 0
sum3 = 0
sum4 = 0
G = nx.Graph()


def calc_method(edge, node0, node1, G):
    G.remove_edge(node0,node1)
    Jaccard_coefficient(node0,node1,G)
    Geometric_coefficient(node0,node1,G)
    Dice_coefficient(node0,node1,G)
    Simpson_coefficient(node0,node1,G)
    G.add_edge(node0,node1)
    pass


def Jaccard_coefficient(node0,node1,G):
    global sum1
    s1 = number_of_common_neighbors(node0,node1,G)
    degree1 = nx.degree(G,node0)
    degree2 = nx.degree(G,node1)
    res = s1 / (degree1 + degree2 - s1)
    sum1 += res

    pass


def Geometric_coefficient(node0,node1,G):
    global sum2
    s1 = number_of_common_neighbors(node0,node1,G)
    degree1 = nx.degree(G,node0)
    degree2 = nx.degree(G,node1)
    res = (s1*s1+1) / (degree1*degree2 + 1)
    sum2 += res

    pass


def Dice_coefficient(node0,node1,G):
    global sum3
    s1 = number_of_common_neighbors(node0,node1,G)
    degree1 = nx.degree(G,node0)
    degree2 = nx.degree(G,node1)
    res = 2*s1 / (degree1 + degree2)
    sum3 += res

    pass


def Simpson_coefficient(node0,node1,G):
    global sum4
    s1 = number_of_common_neighbors(node0,node1,G)
    degree1 = nx.degree(G,node0)
    degree2 = nx.degree(G,node1)
    res = s1 / (min(degree1,degree2)+1)
    sum4 += res

    pass


def get_edge():
    count = 0
    for edge in G.edges:
        if count >= 1000:
            return
        else:
            node = list(edge)
            # remove_predict(edge)
            node0 = node[0]
            node1 = node[1]
            calc_method(edge, node0, node1, G)
            count += 1
        pass
    pass


def number_of_common_neighbors(u,v,G):
    return len(list(nx.common_neighbors(G, u, v)))
    pass


def neighbors_of_node(G, node):
    return G.neighbors(node)


def number_of_edges(G):
    return nx.number_of_edges(G)


# construct graph
def read_biogrid_human_ppi_cin():
    inputFile = open("biogrid_human_ppi_cln.txt")
    for line in inputFile.readlines():
        line = line.split()
        gene0 = line[0]
        gene1 = line[1]
        G.add_edge(gene0, gene1)

    pass


if __name__ == '__main__':
    read_biogrid_human_ppi_cin()
    get_edge()
    print(sum1 / 1000)
    print(sum2 / 1000)
    print(sum3 / 1000)
    print(sum4 / 1000)

    pass


'''
0.02447478468115027
0.008252738978559042
0.04655488197958296
0.08753723493714088
'''