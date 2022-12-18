#!/usr/bin/env python3
from graph_generator_with_mugs import generate_3_colourable_graph_with_MUGs
from random_graph_generator import generate_random_3_colourable_graph
from colouring import colour_graph, check_if_correctly_coloured, GraphColouringError
from params import graphs_to_generate, max_embedding_iterations
from data_renderer import render_data

import random


def run_once_with_MUGs(max_embeddings):
    # Generate how may embedding we will do
    embedding_iterations = random.randint(1, max_embeddings) if max_embeddings > 1 else 1

    # We will produce a graph with v_count vertexes
    G = generate_3_colourable_graph_with_MUGs(embedding_iterations)

    # colours[i] = colour of vertex with number i
    colours = colour_graph(G)

    # Prints how many colours we used
    number_of_colours = check_if_correctly_coloured(G, colours)
    if not number_of_colours:
        raise GraphColouringError

    return G.shape[0], number_of_colours

def run():
    statistics, vertexes_data, colours_data = list(), list(), list()
    asymp = list()
    for i in range(graphs_to_generate):
        vertexes, colours = run_once_with_MUGs(max_embedding_iterations)
        n = colours/(vertexes ** 0.5)
        asymp.append(n)
        vertexes_data.append(vertexes)
        colours_data.append(colours)
        statistics.append((vertexes, colours))

    render_data(vertexes_data, colours_data, max_embedding_iterations)
    print(max(asymp))

run()
