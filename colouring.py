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


def colour_vertexes_with_queue(G, colours, v_i_neighbours):
    # Pick new colour (especially two, new_colour and new_colour + 1)
    new_colour = np.amax(colours) + 1

    # Iterate all v_i_neighbours because they may form a few sepatated groups
    for v_first in v_i_neighbours:
        # For each vertex prepare a queue...
        vertexes_queue = list()
        colours[v_first] = new_colour
        vertexes_queue.append(v_first)

        while vertexes_queue:
            # ... which will be used to spread the colours. Take a vertex from the top of the queue
            v_current = vertexes_queue.pop(-1)
            for j in v_i_neighbours:
                # If it has a coloured neighbour, colour it in the different colour
                if G[v_current][j] and colours[j]:
                    colours[v_current] = new_colour if colours[j] != new_colour else new_colour + 1
                # Otherwise, add it to the top of the queue
                elif G[v_current][j] and not colours[j] and j not in vertexes_queue:
                    vertexes_queue.append(j)


def colour_v_with_neighbours_and_get_them_out(G, v_i, colours):
    v_count = G.shape[0]

    # Collect v_i neighbours
    v_i_neighbours = np.array([], dtype=int)
    for i in range(v_count):
        if G[v_i][i]:
            v_i_neighbours = np.append(v_i_neighbours, i)

    # Use first colour of all to colour v_i
    colours[v_i] = 1

    # v_i and v_i_neighbours form a 3-colourable graph, where v_i is connected
    # with all of them; so for v_i_neighbours without v_i we may perform a
    # colouring in two new colours, which is simply
    colour_vertexes_with_queue(G, colours, v_i_neighbours)

    # Lastly, we have to delete all edges adjacent to v_i and v_i_neighbours
    v_i_neighbours = np.append(v_i_neighbours, v_i)
    for i in v_i_neighbours:
        for j in range(v_count):
            G[i][j] = 0
            G[j][i] = 0


def greedy_colouring(G, colours):
    v_count = G.shape[0]

    # Pick new colour
    min_unused_colour = np.amax(colours) + 1

    # Get uncoloured vertexes. All coloured now have no edges adjanced to them
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

    # Lastly, we perform a greedy colouring algorithm for all uncoloured vertexes
    greedy_colouring(G, colours)

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
