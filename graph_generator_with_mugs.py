from mugs import MUGs
from params import MAX_EMBEDDING_ITERATIONS

import numpy as np
import random


def pick_random_edge_with_left_degree_less_4(G):
    v_count = G.shape[0]
    # Compute vertexes degrees by summing ones in matrix
    v_degrees = np.sum(G, axis=0)

    while True:
        random_vertex = random.randint(0, v_count-1)

        # If this failed, we pick next random vertex
        if v_degrees[random_vertex] <= 3:
            # Get all vertexes which are connected with random_vertex
            random_vertex_neighbours = np.array([], dtype=int)
            for j in range(v_count):
                if G[random_vertex][j] == 1:
                    random_vertex_neighbours = np.append(random_vertex_neighbours, j)

            if not random_vertex_neighbours.size:
                continue
            # Pick one of vertexes from random_vertex_neighbours
            second_vertex = random.choice(random_vertex_neighbours)
            if random_vertex > second_vertex:
                return [random_vertex, second_vertex]

            return [second_vertex, random_vertex]


def embed_random_MUG(G, random_MUG, G_edge):
    G_v_count = G.shape[0]
    G_merged = G_edge[0]
    merged_data_from_G = np.delete(G[G_merged], G_merged, 0)

    MUG_v_count = random_MUG.shape[0]
    MUG_edge = pick_random_edge_with_left_degree_less_4(random_MUG)
    MUG_merged = MUG_edge[0]
    merged_data_from_MUG = np.delete(random_MUG[MUG_merged], MUG_merged, 0)

    # Prepare a matrix to combine these two graphs; it will have one vertex less than G and MUG in sum
    new_G_v_count = G_v_count + MUG_v_count - 1
    new_G = np.zeros((new_G_v_count, new_G_v_count))

    # According to the algorithm, we will merge G_merged vertex and MUG_edge[0] vertex.
    # So, new graph will have this matrix
    #                              |                 |
    #       G matrix w/o merged    |  merged from G  | G_edge[1] <-> MUG_edge[1]
    #   ---------------------------|-----------------|---------------------------
    #           merged from G      |        0        |       merged from MUG
    #   ---------------------------|-----------------|---------------------------
    #    G_edge[1] <-> MUG_edge[1] | merged from MUG |   MUG matrix w/o merged
    #                              |                 |

    # G matrix w/o merged
    G = np.delete(G, G_merged, axis=0)
    G = np.delete(G, G_merged, axis=1)
    for i in range(G_v_count-1):
        for j in range(G_v_count-1):
            new_G[i][j] = G[i][j]

    # MUG matrix w/o merged
    random_MUG = np.delete(random_MUG, MUG_merged, axis=0)
    random_MUG = np.delete(random_MUG, MUG_merged, axis=1)
    for i in range(MUG_v_count-1):
        for j in range(MUG_v_count-1):
            new_G[G_v_count + i][G_v_count + j] = random_MUG[i][j]

    # merged from G
    for i in range(G_v_count-1):
        new_G[G_v_count - 1][i] = merged_data_from_G[i]
        new_G[i][G_v_count - 1] = merged_data_from_G[i]

    # merged with random_MUG
    for i in range(MUG_v_count-1):
        new_G[G_v_count - 1][G_v_count + i] = merged_data_from_MUG[i]
        new_G[G_v_count + i][G_v_count - 1] = merged_data_from_MUG[i]

    # G_edge[1] <-> MUG_edge[1]
    new_G[G_v_count + MUG_edge[1]][G_edge[1]] = 1
    new_G[G_edge[1]][G_v_count + MUG_edge[1]] = 1

    # remove edges between G_edge[0] and G_edge[1], between MUG_edge[0] and MUG_edge[1]
    new_G[G_v_count - 1][G_edge[1]] = 0
    new_G[G_edge[1]][G_v_count - 1] = 0

    new_G[G_v_count - 1][G_v_count + MUG_edge[1]] = 0
    new_G[G_v_count + MUG_edge[1]][G_v_count - 1] = 0

    return new_G


def generate_3_colourable_graph_with_MUGs():
    embedding_iterations = random.randint(1, MAX_EMBEDDING_ITERATIONS)

    # Prepare an initial matrix. For example, any of MUGs
    G = random.choice(MUGs)
    # show_graph_with_labels(G)

    for w in range(embedding_iterations):
        G_edge = pick_random_edge_with_left_degree_less_4(G)

        random_MUG = random.choice(MUGs)
        # show_graph_with_labels(random_MUG)

        G = embed_random_MUG(G, random_MUG, G_edge)
        # show_graph_with_labels(G)

    return G
