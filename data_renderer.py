#!/usr/bin/env python3
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


# For any use
def show_graph_with_labels(adjacency_matrix):
    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=200, with_labels=True)
    plt.show()

def render_data(vertexes_data, colours_data, max_embedding_iterations):
    plt.scatter(vertexes_data, colours_data)
    plt.plot([i for i in range(max_embedding_iterations*11)], [(j ** 0.5) * 3 for j in range(max_embedding_iterations*11)])
    plt.plot([i for i in range(max_embedding_iterations*11)], [(j ** 0.5) * 2.1 for j in range(max_embedding_iterations*11)])
    plt.show()
