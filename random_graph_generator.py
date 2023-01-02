from params import P_TO_PLACE_AN_EDGE, VERTEXES_MIN, VERTEXES_MAX
from data_renderer import show_graph_with_labels
import numpy as np
import random


def delete_extra_edges(G):
    return G

def generate_random_3_colourable_graph():
    # How many vertexes will there be?
    v_count = random.randint(VERTEXES_MIN, VERTEXES_MAX)

    # Prepare an initial matrix
    G = np.zeros((v_count, v_count))

    for i in range(v_count):
        for j in range(i):
            to_be_or_not_to_be = random.random()
            if to_be_or_not_to_be <= P_TO_PLACE_AN_EDGE:
                G[i][j] = 1
                G[j][i] = 1
    
    G = delete_extra_edges(G)
    
    # show_graph_with_labels(G)
    return G
