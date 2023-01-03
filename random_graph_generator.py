from params import P_TO_PLACE_AN_EDGE, VERTEXES_MIN, VERTEXES_MAX
from data_renderer import show_graph_with_labels
import numpy as np
import random


def delete_extra_edges(G):
    v_count = G.shape[0]
    colours = np.zeros((v_count,))

    for v_i in range(v_count):
        colour_for_v_i = v_i % 3 + 1

        # Delete edges which connect v_i with the vertexes of the chosen
        for j in range(v_count):
            if G[v_i][j] and colours[j] == colour_for_v_i:
                G[v_i][j] = 0
                G[j][v_i] = 0
            
        colours[v_i] = colour_for_v_i


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
    
    delete_extra_edges(G)

    return G
