import aocd
import re

EXAMPLE = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip()

class Node:

    def __init__(self, id):

        self.id = id
        self.children = []

def find_interconnected_computers(nodes):

    def recur(connections):

        if len(connections) == 3:
            if connections[0] in nodes[connections[-1]].children:
                return set([tuple(sorted(connections))])
            else:
                return set()

        all = set()
        for id in nodes[connections[-1]].children:
            if id not in connections:
                all = all | recur(connections + [id])
        
        return all

    all = set()
    for id in nodes.keys():
        all = all | recur([id])
    return all

def find_largest_connections(nodes):

    networks = [set([id]) for id in nodes.keys()]
    for i, network in enumerate(networks):
        for id, node in nodes.items():
            if network - set(node.children) == set():
                networks[i].add(id)

    
    best = None
    for network in networks:
        if best is None or len(network) > len(best):
            best = network
    return best

if __name__ == "__main__":

    _in = EXAMPLE
    _in = aocd.get_data(year = 2024, day = 23)

    # Parse Input
    pairs = []
    for line in _in.split("\n"):
        match = re.match(r"([a-z]{2})-([a-z]{2})", line)
        pairs += [(match.group(1), match.group(2))]

    nodes = {}
    for left_id, right_id in pairs:

        if left_id not in nodes:
            left_node = Node(left_id)
            nodes[left_id] = left_node
        else:
            left_node = nodes[left_id] 
        left_node.children += [right_id]

        if right_id not in nodes:
            right_node = Node(right_id)
            nodes[right_id] = right_node
        else:
            right_node = nodes[right_id]
        right_node.children += [left_id]
 
    # Part 1
    connections = find_interconnected_computers(nodes)
    connections = list(filter(lambda x: x[0][0] == "t" or x[1][0] == "t" or x[2][0] == "t", connections))
    print(len(connections))

    # Part 2
    connections = find_largest_connections(nodes)
    print(",".join(sorted(connections)))