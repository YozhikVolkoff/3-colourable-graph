#!/usr/bin/env python3
from params import total_number, number_to_place_an_edge
from data_renderer import show_graph_with_labels
import numpy as np
import random


def delete_extra_edges(G):
    return G

def generate_random_3_colourable_graph(n):
    # Prepare an initial matrix. For example, any of MUGs
    G = np.zeros((n, n))
    # show_graph_with_labels(G)

    for i in range(n):
        for j in range(i):
            to_be_or_not_to_be = random.randint(1, total_number)
            if to_be_or_not_to_be <= number_to_place_an_edge:
                G[i][j] = 1
                G[j][i] = 1
    
    G = delete_extra_edges(G)
    
    show_graph_with_labels(G)
    return G

for i in range(10):
    generate_random_3_colourable_graph(15)
