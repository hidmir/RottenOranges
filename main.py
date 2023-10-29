import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
from matplotlib.pyplot import get_cmap

# Initial data
v = [[2, 1, 0, 2, 1],
     [1, 0, 1, 2, 1],
     [1, 0, 0, 2, 1]]

rows, cols = len(v), len(v[0])

G = nx.Graph()


def get_node_id(row, col):
    return row * cols + col


for i in range(rows):
    for j in range(cols):
        G.add_node(get_node_id(i, j), value=v[i][j])
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            x, y = i + dx, j + dy
            if 0 <= x < rows and 0 <= y < cols:
                G.add_edge(get_node_id(i, j), get_node_id(x, y))


def draw_graph(title):
    pos = {node: (node % cols, rows - node // cols - 1) for node in G.nodes()}
    colors = [G.nodes[node]['value'] for node in G.nodes()]
    labels = {node: G.nodes[node]['value'] for node in G.nodes()}
    nx.draw(G, pos, node_color=colors, labels=labels, with_labels=True, cmap=get_cmap(name='rainbow'), vmin=0, vmax=2)
    plt.title(title)
    plt.show()


draw_graph("Initial State")

time = 0
rotten_queue = deque([node for node, attr in G.nodes(data=True) if attr['value'] == 2])

while rotten_queue:
    new_rotten = deque()
    while rotten_queue:
        current = rotten_queue.popleft()
        for neighbor in G.neighbors(current):
            if G.nodes[neighbor]['value'] == 1:
                G.nodes[neighbor]['value'] = 2
                new_rotten.append(neighbor)
    if new_rotten:
        time += 1
        rotten_queue = new_rotten
        draw_graph(f"After {time} Iterations")

if any(attr['value'] == 1 for _, attr in G.nodes(data=True)):
    print("Not all oranges can be rotten.")
else:
    print(f"All oranges can be rotten in {time} time units.")
