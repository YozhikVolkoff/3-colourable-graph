#!/usr/bin/env python3

from MUGs import MUG_9, MUG_10, MUG_11a, MUG_11b, MUG_12a # MUG_12b, MUG_12c
from params import graphs_to_generate, max_embedding_iterations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random


# Append all MUGs to array to pisk from
MUGS = [MUG_9, MUG_10, MUG_11a, MUG_11b, MUG_12a] #MUG_12b, MUG12c


def show_graph_with_labels(adjacency_matrix):
    rows, cols = np.where(adjacency_matrix == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=200, with_labels=True)
    plt.show()


def pick_random_edge_with_left_degree_less_4(G):
    v_count = G.shape[0]
    # Compute vertexes degrees by summing ones in matrix
    v_degrees = np.sum(G, axis=0)

    while True:
        random_vertex = random.randint(0, v_count-1)

        # If this failed, we pick next random vertex
        if v_degrees[random_vertex] <= 3:
            # Get all vertexes which are connected with random_vertex
            random_vertex_neighbours = []
            for j in range(v_count):
                if G[random_vertex][j] == 1:
                    random_vertex_neighbours.append(j)

            if not random_vertex_neighbours:
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


def generate_3_colourable_graph(embedding_iterations):
    # Prepare an initial matrix. For example, any of MUGS
    G = random.choice(MUGS)
    # G = np.array([
    #     [0, 1, 0],
    #     [1, 0, 1],
    #     [0, 1, 0],
    # ])
    # show_graph_with_labels(G)

    for w in range(embedding_iterations):
        G_edge = pick_random_edge_with_left_degree_less_4(G)

        random_MUG = random.choice(MUGS)
        # random_MUG = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]]) 
        # show_graph_with_labels(random_MUG)

        G = embed_random_MUG(G, random_MUG, G_edge)
        # show_graph_with_labels(G)

    return G


def find_vertex_with_degree_more_then_square_of_n(G, n):
    # Count vertexes degree by sum
    v_degrees = np.sum(G, axis=0)
    square_of_n = int(n ** 0.5)

    # Check if there is a vertex with degree more then n ** 0.5 in graph G
    for i in range(n):
        if v_degrees[i] >= square_of_n:
            return i
    
    # If there is not, return nothing
    return None


def colour_v_with_neighbours_and_get_them_out(G, v_i, colours):
    v_count = G.shape[0]

    # Find all vertexes v_i is connected with
    v_i_neighbours = []
    for i in range(v_count):
        if G[v_i][i] == 1:
            v_i_neighbours.append(i)
    
    # Use first colour of all to colour v_i
    colours[v_i] = 1
    # Pick new possible colour and colour the main vertex, v_i
    new_colour = max(colours) + 1

    # v_i and v_i_neighbours form a 3-colourable graph, where v_i is connected
    # with all of them; so for v_i_neighbours without v_i we may perform a
    # colouring in two new colours, which is simply
    for v_current in v_i_neighbours:
        may_colour_in_new_colour = True
        # We check only vertexes in v_i_neighbours, other will have other colours
        for j in v_i_neighbours:
            if G[v_current][j] == 1 and colours[j] == (new_colour):
                may_colour_in_new_colour = False
                break

        if may_colour_in_new_colour:
            colours[v_current] = new_colour
        else:
            colours[v_current] = new_colour + 1

    # Lastly, we have to delete all edges adjacent to v_i or v_i_neighbours
    v_i_neighbours.append(v_i)
    for i in v_i_neighbours:
        for j in range(v_count):
            G[i][j] = 0
            G[j][i] = 0


def colour_graph(G_input):
    v_count = G_input.shape[0]
    # Prepare an array for colours, 0 = not coloured
    colours = np.zeros((v_count,))

    # Full copy the input graph G_input because we will modify it
    G = G_input[[i for i in range(v_count)]]

    # While we may fing the vertex which is connected with at least n ** 0.5 other vertexes,
    # we call colour_v_with_neighbours_and_get_them_out() procedure
    while v_i := find_vertex_with_degree_more_then_square_of_n(G, v_count):
        colour_v_with_neighbours_and_get_them_out(G, v_i, colours)
        v_i = find_vertex_with_degree_more_then_square_of_n(G, v_count)
    
    # Lastly, we perform a greedy colouring algorithm. All vertexes have
    # degree less than (n ** 0.5), so we need this number of colours.
    min_unused_colour = max(colours) + 1

    # Get uncoloured vertexes. All coloured now have no edges adjanced to them, so we wiil count degrees
    last_vertexes = list()
    v_degrees = np.sum(G, axis=0)
    for i in range(v_count):
        if colours[i] == 0:
            last_vertexes.append(i)

    for v_current in last_vertexes:
        # Collect v_current neighbours' colours
        neighbours_colours = set()
        for j in range(v_count):
            if G[v_current][j] == 1 and colours[j] != 0:
                neighbours_colours.add(colours[j])
        
        # Find the first colour which is not used by neighbours
        min_acceptable_colour = min_unused_colour
        while min_acceptable_colour in neighbours_colours:
            min_acceptable_colour += 1

        colours[v_current] = min_acceptable_colour

    return colours


def check_if_correctly_coloured(G_coloured, colours):
    # Find which vertexes do edges connect
    G_edges = np.nonzero(G_coloured == 1)
    list_of_coordinates = list(zip(G_edges[0], G_edges[1]))

    # For each edge check if its bounds have the same colour
    for elem in list_of_coordinates:
        if colours[elem[0]] == colours[elem[1]]:
            print('Wrong colouring', elem[0], elem[1], colours[elem[0]])
            return False

    # If we didn't return False, then we return 
    return max(colours)


def run_once(max_embeddings):
    # Generate how may embedding we will do
    embedding_iterations = random.randint(1, max_embeddings) if max_embeddings > 1 else 1

    # We will produce a graph with v_count vertexes
    G = generate_3_colourable_graph(embedding_iterations)

    # colours[i] = colour of vertex with number i
    colours = colour_graph(G)

    # Prints how many colours we used
    number_of_colours = check_if_correctly_coloured(G, colours)
    # print(f'On graph with {G.shape[0]} vertexes we spend {number_of_colours} colours')
    return G.shape[0], number_of_colours


statistics, vertexes_data, colours_data = list(), list(), list()
asymp = list()
for i in range(graphs_to_generate):
    vertexes, colours = run_once(max_embedding_iterations)
    n = colours/(vertexes ** 0.5)
    asymp.append(n)
    vertexes_data.append(vertexes)
    colours_data.append(colours)
    statistics.append((vertexes, colours))


plt.scatter(vertexes_data, colours_data)
plt.plot([i for i in range(max_embedding_iterations*11)], [(j ** 0.5) * 3 for j in range(max_embedding_iterations*11)])
plt.plot([i for i in range(max_embedding_iterations*11)], [(j ** 0.5) * 2.1 for j in range(max_embedding_iterations*11)])
plt.show()
print(max(asymp))
