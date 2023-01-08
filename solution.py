import ast
import numpy as np


def levenshteinDistance(s1, s2):
    m = np.zeros((len(s1)+1, len(s2)+1))
    for i in range(len(s1)+1):
        m[i][0] = i
    for j in range(len(s2)+1):
        m[0][j] = j
    for i, c1 in enumerate(s1):
        for j, c2 in enumerate(s2):
            cost = 0 if c1 == c2 else 1
            m[i+1][j+1] = min(m[i][j+1]+1, m[i+1][j]+1, m[i][j]+cost)
    return int(m[len(s1)][len(s2)])

def normalize_file(filename):
    with open(filename) as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        for field, value in ast.iter_fields(node):
            if isinstance(value, str):
                value = value.strip()
            elif isinstance(value, (int, float)):
                value = str(value)
            setattr(node, field, value)
    return ast.dump(tree)

def plagiarism_score(tree1, tree2):
    distance = levenshteinDistance(normalize_file(tree1), normalize_file(tree2))
    tree1=ast.parse(open(tree1).read())
    tree2=ast.parse(open(tree2).read())
    num_nodes = sum(1 for _ in ast.walk(tree1)) + sum(1 for _ in ast.walk(tree2))
    print(distance, num_nodes)
    return 1 - distance / max(len(tree1.body), len(tree2.body))

def parseInput(input):
    scores = open("scores.txt", "w")
    file = open(input, "r");
    text = file.readlines();
    for i in text:
        comparables = i.split()
        if len(comparables)==2:
            scores.write(str(plagiarism_score(comparables[0], comparables[1])) + "\n")
parseInput("input.txt")