import aocd
import re

EXAMPLE="""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""".strip()

EXAMPLE2 = """
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""".strip()

EXAMPLE3 = """
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""".strip()

class Node:

    def __init__(self, label):

        self.label = label
        self.children = []

def count_all_paths(nodes, start, end, allow_revisits = False):

    def depth_first_search(node, path = [], allow_revisits = False):
        
        if path and path[-1] == end:
            return [path]

        paths = []
        for child in node.children:

            if child == start:
                continue
            elif allow_revisits and child.lower() == child and sum([1 if child == el else 0 for el in path]) == 1:
                paths += depth_first_search(nodes[child], path + [child], False)
            elif child.lower() == child and child in path:
                continue
            else:
                paths += depth_first_search(nodes[child], path + [child], allow_revisits)

        return paths

    return len(depth_first_search(nodes[start], [start], allow_revisits))


if __name__ == "__main__":

    input = aocd.get_data(day = 12, year = 2021)
    nodes = {}
    for line in input.split("\n"):
        match = re.match("([a-zA-Z]+)-([a-zA-Z]+)", line.strip())
        left_label = match.group(1)
        right_label = match.group(2)

        if left_label not in nodes:
            nodes[left_label] = Node(left_label)
        
        if right_label not in nodes:
            nodes[right_label] = Node(right_label)

        nodes[left_label].children += [right_label]
        nodes[right_label].children += [left_label]

    # Part 1
    print(count_all_paths(nodes, "start", "end"))
    
    # Part 2
    print(count_all_paths(nodes, "start", "end", True))