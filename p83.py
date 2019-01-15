""" Problem 83

NOTE: This problem is a more challenging version of Problem 81.

In the 5 by 5 matrix below, the minimal path sum from the top left to the
bottom right, by moving left, right, up, and down, is indicated in bold red
and is equal to 2297.

    131  673  234--103--018
     |         |         |
    201--096--342  965  150
                         |
    630  803  746  422--111
                    |
    537  699  497  121  956
                    |
    805  732  524  037--311

Find the minimal path sum in the 80 by 80 matrix, from the left column to the
right column."""

import utils.graph

def load_file(filename):
    """ Takes filename of line separated rows of comma-separated entries.

    Returns a tuple (graph, start, end) with:
        - graph: a digraph with edges encoding the rules of only moving down
                 or up or right, and nodes created from the csv values.
        - start: a special start node
        - end:   a special end node
    """
    # Create matrix from csv lines
    with open(filename) as f:
        m = [list(map(int, line.split(','))) for line in f]
    # Create digraph from matrix
    graph = utils.graph.DiGraph()
    ROWS = len(m)
    COLS = len(m[0])
    for r in range(ROWS):
        for c in range(COLS):
            u = (r, c)
            # Add the node to the left
            if 0 <= c-1:
                v = (r, c-1)
                weight = m[r][c-1]
                graph.add_edge(u, v, weight)
            # Add the node to the right
            if c+1 < COLS:
                v = (r, c+1)
                weight = m[r][c+1]
                graph.add_edge(u, v, weight)
            # Add add to node below
            if r+1 < ROWS:
                v = (r+1, c)
                weight = m[r+1][c]
                graph.add_edge(u, v, weight)
            # Add add to node above
            if 0 <= r-1:
                v = (r-1, c)
                weight = m[r-1][c]
                graph.add_edge(u, v, weight)
    # also add a start element and edge to top-left elem
    start_node = 'START'
    weight = m[0][0]
    graph.add_edge(start_node, (0,0), weight)
    # also add an end element and edge from the bottom right elem
    end_node = 'END'
    weight = 0
    graph.add_edge((ROWS-1, COLS-1), end_node, weight)
    return graph, start_node, end_node

def ANSWER():
    graph, start, end = load_file('matrix.txt')
    path = utils.graph.dijkstra(graph, start, end)
    path_cost = utils.graph.path_cost(graph, path)
    return path_cost

def TEST():
    expect = [131, 201, 96, 342, 234, 103, 18, 150, 111, 422, 121, 37, 331]
    graph, start, end = load_file('matrix_test.txt')
    actual = utils.graph.dijkstra(graph, start, end)
    actual_cost = utils.graph.path_cost(graph, actual)
    print('ACTUAL:', actual, '=', actual_cost)
    print('EXPECT:', expect, '=', sum(expect))

if __name__ == '__main__':
    import utils
    #TEST()
    utils.solution_printer(ANSWER)



