import numpy as np


class GraphColouringError(BaseException):
    pass


def find_vertex_with_degree_more_then_square_of_n(G, n):
    # Count vertexes degree by sum
    v_degrees = np.sum(G, axis=0)
    square_of_n = int(n ** 0.5)

    # Check if there is a vertex with degree more then n ** 0.5 in graph G
    for i in range(n):
        if v_degrees[i] >= square_of_n:
            return i
    
    # If there is not, return -1
    return -1


def colour_a_part_of_G_in_2_colours(G, v_i_neighbours, colours):
    # Pick new possible colour
    new_colour = max(colours) + 1

    for v_current in v_i_neighbours:
        may_colour_in_new_colour = True
        # We check only vertexes in v_i_neighbours, other will have other colours
        for j in v_i_neighbours:
            if G[v_current][j] == 1 and colours[j] == new_colour:
                may_colour_in_new_colour = False
                break

        if may_colour_in_new_colour:
            colours[v_current] = new_colour
        else:
            colours[v_current] = new_colour + 1


def colour_v_with_neighbours_and_get_them_out(G, v_i, colours):
    v_count = G.shape[0]

    # Find all vertexes v_i is connected with
    v_i_neighbours = list()
    for i in range(v_count):
        if G[v_i][i] == 1:
            v_i_neighbours.append(i)

    # Use first colour of all to colour v_i
    colours[v_i] = 1

    # v_i and v_i_neighbours form a 3-colourable graph, where v_i is connected
    # with all of them; so for v_i_neighbours without v_i we may perform a
    # colouring in two new colours, which is simply
    colour_a_part_of_G_in_2_colours(G, v_i_neighbours, colours)

    # Lastly, we have to delete all edges adjacent to v_i and v_i_neighbours
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
    v_i = find_vertex_with_degree_more_then_square_of_n(G, v_count)
    while v_i >= 0:
        colour_v_with_neighbours_and_get_them_out(G, v_i, colours)
        v_i = find_vertex_with_degree_more_then_square_of_n(G, v_count)

    # Lastly, we perform a greedy colouring algorithm
    min_unused_colour = max(colours) + 1

    # Get uncoloured vertexes. All coloured now have no edges adjanced to them, so we will count degrees
    last_vertexes = list()
    for i in range(v_count):
        if colours[i] == 0:
            last_vertexes.append(i)

    for v_current in last_vertexes:
        # Collect v_current neighbours' colours
        neighbours_colours = set()
        for j in range(v_count):
            if G[v_current][j] == 1 and colours[j] != 0:
                neighbours_colours.add(colours[j])
        
        # Find colour which is not used by neighbours
        acceptable_colour = min_unused_colour
        while acceptable_colour in neighbours_colours:
            acceptable_colour += 1

        colours[v_current] = acceptable_colour

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

    # If we didn't return False, then we return max colour number used
    return max(colours)
