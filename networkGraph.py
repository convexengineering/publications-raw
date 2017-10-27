from collections import defaultdict
linksets = defaultdict(set)
links = defaultdict(int)
for constraint in m.flat(constraintsets=False):
    for varkey in constraint.varkeys:
        linksets[varkey].update(constraint.varkeys)
        for varkey2 in constraint.varkeys:
            if varkey2.name != varkey.name:
                links[(varkey.name, varkey2.name)] += 1
for key in linksets:
    linksets[key].remove(key)

print linksets

import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph, labels=None, graph_layout='spring',
               node_size=600, node_color='white', node_alpha=0.7,
               node_text_size=12,
               edge_color='black', edge_alpha=0.3, edge_thickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    # create networkx graph
    G=nx.Graph()

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # these are different layouts for the network you may try
    # shell seems to work best
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    # draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size,
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=graph.values(),
                           alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)

    # show graph
    plt.show()

print links
draw_graph(links)