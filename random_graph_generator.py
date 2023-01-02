from params import P_TO_PLACE_AN_EDGE, VERTEXES_MIN, VERTEXES_MAX
from data_renderer import show_graph_with_labels
import numpy as np
import random


def delete_extra_edges(G_input):
    v_count = G_input.shape[0]
    G = G_input[[i for i in range(v_count)]]
    colours = np.zeros((v_count,))

    for v_i in range(v_count):
        # neighbours_colours[i] = number of neighbours which have colour i+1
        neighbours_colours = np.zeros((3,))
        current_colour = 0

        for j in range(v_count):
            current_colour = int(colours[j])
            if G[v_i][j] == 1 and current_colour:
                neighbours_colours[current_colour - 1] += 1
            
        possible_colours = np.argwhere(neighbours_colours == 0)

        # If there is one or more free colour which may be used, use it for v_i
        if possible_colours.size > 0:
            colours[v_i] = possible_colours[0][0] + 1
            continue
        # Else choose the colour which is used lowly among v_i neighbours
        else:
            min_possible_colour = np.amin(neighbours_colours)
            colour_for_v_i = np.argwhere(neighbours_colours == min_possible_colour)[0][0] + 1

            # Delete edges which connect v_i with the vertexes of the chosen
            for j in range(v_count):
                if G[v_i][j] == 1 and colours[j] == colour_for_v_i:
                    G[v_i][j] = 0
                    G[j][v_i] = 0
            
            colours[v_i] = colour_for_v_i

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
    
    return G
