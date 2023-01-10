from params import MAX_EMBEDDING_ITERATIONS, VERTEXES_MAX

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


ALPHA = 0.5


# For any use
def show_graph_with_labels(adjacency_matrix):
    rows, cols = np.where(adjacency_matrix != 0)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=200, with_labels=True)
    plt.show()


def render_data_mugs(vertexes_data, colours_data, asymp_mugs):
    plt.scatter(vertexes_data, colours_data, c='red', alpha=ALPHA, edgecolors='none')
    plt.plot([i for i in range((MAX_EMBEDDING_ITERATIONS+1)*12)], [(j ** 0.5) * 3 for j in range((MAX_EMBEDDING_ITERATIONS+1)*12)])
    plt.plot([i for i in range((MAX_EMBEDDING_ITERATIONS+1)*12)], [(j ** 0.5) * asymp_mugs for j in range((MAX_EMBEDDING_ITERATIONS+1)*12)], 'black')
    plt.xlabel("Number of vertexes is graph")
    plt.ylabel("Number of used colours")
    plt.title("Colours usage, generation with embedding")
    plt.grid()
    plt.show()


def render_data_random(vertexes_data, colours_data, asymp_random, average_random):
    plt.scatter(vertexes_data, colours_data, c='green', alpha=ALPHA, edgecolors='none')
    plt.plot([i for i in range(VERTEXES_MAX+1)], [(j ** 0.5) * 3 for j in range(VERTEXES_MAX+1)])
    plt.plot([i for i in range(VERTEXES_MAX+1)], [(j ** 0.5) * asymp_random for j in range(VERTEXES_MAX+1)], 'black')
    plt.plot([i for i in range(VERTEXES_MAX+1)], [(j ** 0.5) * average_random for j in range(VERTEXES_MAX+1)],'r')
    plt.xlabel("Number of vertexes is graph")
    plt.ylabel("Number of used colours")
    plt.title("Colours usage, random generation")
    plt.grid()
    plt.show()
