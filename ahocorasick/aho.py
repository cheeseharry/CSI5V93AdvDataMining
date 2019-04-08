import os
import sys
import argparse


class AhoNode:
    def __init__(self):
        self.goto = {}
        self.out = []
        self.fail = None


def aho_create_forest(patterns):
    root = AhoNode()

    for path in patterns:
        node = root
        for symbol in path:
            node = node.goto.setdefault(symbol, AhoNode())
        node.out.append(path)
    return root


def aho_create_statemachine(patterns):
    root = aho_create_forest(patterns)
    queue = []
    for node in root.goto.values():
        queue.append(node)
        node.fail = root

    while len(queue) > 0:
        rnode = queue.pop(0)

        for key, unode in rnode.goto.items():
            queue.append(unode)
            fnode = rnode.fail
            while fnode is not None and key not in fnode.goto.keys():
                fnode = fnode.fail
            unode.fail = fnode.goto[key] if fnode else root
            unode.out += unode.fail.out

    return root


def aho_find_all(s, root, callback):
    node = root

    for i in range(len(s)):
        while node is not None and s[i] not in node.goto.keys():
            node = node.fail
        if node is None:
            node = root
            continue
        node = node.goto[s[i]]
        for pattern in node.out:
            callback(i - len(pattern) + 1, pattern)


############################
# Demonstration of work
def on_occurence(pos, patterns):
    print("At pos %s found pattern: %s" % (pos, patterns))
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
        pattern_list.append(line)
        pass

    return pattern_list
    pass


if __name__ == '__main__':
    arglist = sys.argv
    print(arglist[1])
    patterns = ['test', 'estes', 'stes']
    s = "testestest"
    root = aho_create_statemachine(patterns)
    aho_find_all(s, root, on_occurence)
    pass
