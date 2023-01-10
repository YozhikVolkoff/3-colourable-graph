from graph_generator_with_mugs import generate_3_colourable_graph_with_MUGs
from random_graph_generator import generate_random_3_colourable_graph
from colouring import colour_graph, check_if_correctly_coloured, GraphColouringError
from params import GRAPHS_TO_GENERATE
from data_renderer import render_data_mugs, render_data_random

from tqdm import tqdm
import numpy as np


def run_once_with_MUGs():
    G = generate_3_colourable_graph_with_MUGs()

    # colours[i] = colour of vertex with number i
    colours = colour_graph(G)

    # Get how many colours we used
    number_of_colours = check_if_correctly_coloured(G, colours)
    if not number_of_colours:
        raise GraphColouringError

    return G.shape[0], number_of_colours


def run_once_with_random_generator():
    # Just another function to separate randomly genetared prahps
    G = generate_random_3_colourable_graph()

    colours = colour_graph(G)

    number_of_colours = check_if_correctly_coloured(G, colours)
    if not number_of_colours:
        raise GraphColouringError

    return G.shape[0], number_of_colours


def run():
    vertexes_mugs, colours_mugs = np.empty([GRAPHS_TO_GENERATE], dtype=int), np.empty([GRAPHS_TO_GENERATE], dtype=int)
    vertexes_random, colours_random = np.empty([GRAPHS_TO_GENERATE], dtype=int), np.empty([GRAPHS_TO_GENERATE], dtype=int)
    asymp_mugs, asymp_random, average_MUGs, average_random = 0, 0, 0, 0

    for i in tqdm(range(GRAPHS_TO_GENERATE)):
        vertexes, colours = run_once_with_MUGs()
        n = colours/(vertexes ** 0.5)
        asymp_mugs = n if n > asymp_mugs else asymp_mugs
        average_MUGs += n/GRAPHS_TO_GENERATE
        vertexes_mugs[i] = vertexes
        colours_mugs[i] = colours

        vertexes, colours = run_once_with_random_generator()
        n = colours/(vertexes ** 0.5)
        asymp_random = n if n > asymp_random else asymp_random
        average_random += n/GRAPHS_TO_GENERATE
        vertexes_random[i] = vertexes
        colours_random[i]= colours

    render_data_mugs(vertexes_mugs, colours_mugs, asymp_mugs)
    render_data_random(vertexes_random, colours_random, asymp_random, average_random)
    print("Asymptotic is {} for MUGs generator and {} for random generator".format(asymp_mugs, asymp_random))
    print("Average is {} for MUGs generator and {} for random generator".format(average_MUGs, average_random))

if __name__ == '__main__':
    run()
