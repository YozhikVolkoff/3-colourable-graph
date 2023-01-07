from params import P_TO_PLACE_AN_EDGE, VERTEXES_MIN, VERTEXES_MAX

import numpy as np
import random


def generate_random_3_colourable_graph():
    # How many vertexes will there be?
    v_count = random.randint(VERTEXES_MIN, VERTEXES_MAX)

    # Prepare an initial matrix
    G = np.zeros((v_count, v_count))
    colours = np.zeros((v_count,))

    for v_i in range(v_count):
        # Select colour for current vertex (may be more complicated)
        colour_for_v_i = random.randint(1, 3)
        for j in range(v_i):
            # Skip edge placement if vertexes have the same selected colours
            if colours[j] == colour_for_v_i:
                continue

            # Otherwise, place an edge with the probability specified in the parameters
            to_be_or_not_to_be = random.random()
            if to_be_or_not_to_be <= P_TO_PLACE_AN_EDGE:
                G[v_i][j] = 1
                G[j][v_i] = 1

        colours[v_i] = colour_for_v_i

    return G
