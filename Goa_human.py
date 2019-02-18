# read input and initialize graph
def read_input():
    inputFile = open("goa_human_small.gaf")
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
        ontology = line[6]
        print(gene)
        print(go_term)
        print(ontology)

        pass


if __name__ == '__main__':
    read_input()