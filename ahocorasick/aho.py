import sys

report = open("output_Lei.txt", 'w')


class AcTrieNode:
    def __init__(self):
        self.goto = {}
        self.child = []
        self.failure = None
        pass


def init_Trie(patterns):
    root = AcTrieNode()
    for path in patterns:
        node = root
        for symbol in path:
            node = node.goto.setdefault(symbol, AcTrieNode())
            pass
        node.child.append(path)
        pass
    return root


def state_trans(patterns):
    root = init_Trie(patterns)
    queue = []
    for node in root.goto.values():
        queue.append(node)
        node.failure = root
        pass

    while len(queue) > 0:
        rnode = queue.pop(0)
        for key, unode in rnode.goto.items():
            queue.append(unode)
            fnode = rnode.failure
            pass
            while fnode is not None and key not in fnode.goto.keys():
                fnode = fnode.failure
                pass
            unode.failure = fnode.goto[key] if fnode else root
            unode.child += unode.failure.child
            pass
    return root


def match_pattern(s, root, callback):
    node = root

    for i in range(len(s)):
        while node is not None and s[i] not in node.goto.keys():
            node = node.failure
        if node is None:
            node = root
            continue
        node = node.goto[s[i]]
        for pattern in node.child:
            callback(i - len(pattern) + 1, pattern)
            pass


def write_ouput(index, patterns):
    report.write("At index %s found pattern: %s" % (index, patterns))
    report.write("\n")
    pass


def read_text(text):
    file = open(text)
    fileStr = file.read()
    return fileStr
    pass


def read_pattern(pattern):
    pattern_list = []
    inputFile = open(pattern)
    for line in inputFile.readlines():
        line = line.strip()
        pattern_list.append(line)
        pass

    return pattern_list
    pass


def is_text(filename):
    inputFile = open(filename)
    num = len(inputFile.readlines())

    if num == 1:
        return True
    else:
        return False
    pass


if __name__ == '__main__':
    patterns = []
    text = ""

    arglist = sys.argv

    file1 = arglist[1]
    file2 = arglist[2]

    if is_text(file1):
        text = read_text(file1)
        pass
    else:
        patterns = read_pattern(file1)

    if is_text(file2):
        text = read_text(file2)
        pass
    else:
        patterns = read_pattern(file2)

    root = state_trans(patterns)
    match_pattern(text, root, write_ouput)
    pass
