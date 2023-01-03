import numpy as np


class GraphColouringError(BaseException):
    pass


def find_vertex_with_degree_more_then_square_of_n(G, n):
    # Count vertexes degree by sum
    v_degrees = np.sum(G, axis=0)
    square_of_n = int(n ** 0.5)

    # Check if there is a vertex with degree more then n ** 0.5 in graph G
    result = np.where(v_degrees >= square_of_n)[0]
    if result.size > 0:
        return result[0]
    
    # If there is not, return -1
    return -1


def colour_vertexes_recursively(G, v_i_neighbours, colours, v_current, new_colour, is_white):
    possible_colour = new_colour if is_white else new_colour + 1

    for v in v_i_neighbours:
        if G[v_current][v] and not colours[v]:
            colours[v] = possible_colour
            colour_vertexes_recursively(G, v_i_neighbours, colours, v, new_colour, not is_white)


def colour_v_with_neighbours_and_get_them_out(G, v_i, colours):
    v_count = G.shape[0]

    # Find all vertexes v_i is connected with
    v_i_neighbours = np.array([], dtype=int)
    for i in range(v_count):
        if G[v_i][i]:
            v_i_neighbours = np.append(v_i_neighbours, i)

    # Use first colour of all to colour v_i
    colours[v_i] = 1

    # v_i and v_i_neighbours form a 3-colourable graph, where v_i is connected
    # with all of them; so for v_i_neighbours without v_i we may perform a
    # colouring in two new colours, which is simply
    new_colour = np.amax(colours) + 1

    for v_first in v_i_neighbours:
        if not colours[v_first]:
            colours[v_first] = new_colour
            colour_vertexes_recursively(G, v_i_neighbours, colours, v_first, new_colour, is_white=False)


    # Lastly, we have to delete all edges adjacent to v_i and v_i_neighbours
    v_i_neighbours = np.append(v_i_neighbours, v_i)
    for i in v_i_neighbours:
        for j in range(v_count):
            G[i][j] = 0
            G[j][i] = 0


def colour_graph(G_input):
    v_count = G_input.shape[0]
    # Prepare an array for colours, 0 = not coloured
    colours = np.zeros((v_count,))

    # Full copy the input graph G_input because we will modify it
    G = G_input.copy()

    # While we may fing the vertex which is connected with at least n ** 0.5 other vertexes,
    # we call colour_v_with_neighbours_and_get_them_out() procedure
    v_i = find_vertex_with_degree_more_then_square_of_n(G, v_count)
    while v_i >= 0:
        colour_v_with_neighbours_and_get_them_out(G, v_i, colours)
        v_i = find_vertex_with_degree_more_then_square_of_n(G, v_count)

    # Lastly, we perform a greedy colouring algorithm
    min_unused_colour = np.amax(colours) + 1

    # Get uncoloured vertexes. All coloured now have no edges adjanced to them, so we will count degrees
    last_vertexes = np.array([], dtype=int)
    for i in range(v_count):
        if not colours[i]:
            last_vertexes = np.append(last_vertexes, i)

    for v_current in last_vertexes:
        # Collect v_current neighbours' colours
        neighbours_colours = set()
        for j in range(v_count):
            if G[v_current][j] and colours[j]:
                neighbours_colours.add(colours[j])
        
        # Find colour which is not used by neighbours
        acceptable_colour = min_unused_colour
        while acceptable_colour in neighbours_colours:
            acceptable_colour += 1

        colours[v_current] = acceptable_colour

    return colours


def check_if_correctly_coloured(G_coloured, colours):
    # Find which vertexes do edges connect
    v_count = G_coloured.shape[0]
    for i in range(v_count):
        for j in range(i):
            if colours[i] == colours[j] and G_coloured[i][j]:
                print('Wrong colouring', i, j, colours[i])
                return False

    # If we didn't return False, then we return max colour number used
    return np.amax(colours)
