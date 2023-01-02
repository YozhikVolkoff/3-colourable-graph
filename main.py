from graph_generator_with_mugs import generate_3_colourable_graph_with_MUGs
from random_graph_generator import generate_random_3_colourable_graph
from colouring import colour_graph, check_if_correctly_coloured, GraphColouringError
from params import GRAPHS_TO_GENERATE
from data_renderer import show_graph_with_labels, render_data_mugs, render_data_random


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
    G = generate_random_3_colourable_graph()
    # show_graph_with_labels(G)

    colours = colour_graph(G)

    number_of_colours = check_if_correctly_coloured(G, colours)
    if not number_of_colours:
        raise GraphColouringError

    return G.shape[0], number_of_colours


def run():
    vertexes_mugs, colours_mugs = list(), list()
    vertexes_random, colours_random = list(), list()
    asymp_mugs, asymp_random = 0, 0

    for i in range(GRAPHS_TO_GENERATE):
        vertexes, colours = run_once_with_MUGs()
        n = colours/(vertexes ** 0.5)
        asymp_mugs = n if n > asymp_mugs else asymp_mugs
        vertexes_mugs.append(vertexes)
        colours_mugs.append(colours)

        # vertexes, colours = run_once_with_random_generator()
        # n = colours/(vertexes ** 0.5)
        # asymp_random = n if n > asymp_random else asymp_random
        # vertexes_random.append(vertexes)
        # colours_random.append(colours)

    render_data_mugs(vertexes_mugs, colours_mugs)
    # render_data_random(vertexes_random, colours_random)
    print("Asymptotic is {} for MUGs generator and {} for random generator".format(asymp_mugs, asymp_random))

if __name__ == '__main__':
    run()
