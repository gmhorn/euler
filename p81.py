""" Problem 81

In the 5 by 5 matrix below, the minimal path sum from the top left to the
bottom right, by only moving to the right and down, is indicated in bold red
and is equal to 2427.

    131  673  234  103  013
     |
    201--096--342  965  150
               |
    630  803  746--422  111
                    |
    537  699  497  121  956
                    |
    805  732  524  037--311

Find the minimal path sum in the 80 by 80 matrix, from the top left to the
bottom right by only moving right and down."""

from __future__ import print_function
import euler.utils.graph

def load_file(filename):
    """ Takes filename of line separated rows of comma-separated entries.

    Returns a tuple (graph, start, end) with:
        - graph: a digraph with edges encoding the rules of only moving down
                 and to the right, and nodes created from the csv values.
        - start: the top-left-most value
        - end:   the bottom-right-most value.
    """
    # Create matrix from csv lines
    with open(filename) as f:
        m = [list(map(int, line.split(','))) for line in f]
    # Create digraph from matrix
    graph = euler.utils.graph.DiGraph()
    ROWS = len(m)
    COLS = len(m[0])
    for r in range(ROWS):
        for c in range(COLS):
            u = (r, c)
            if c+1 < COLS:
                v = (r, c+1)
                weight = m[r][c+1]
                graph.add_edge(u, v, weight)
            if r+1 < ROWS:
                v = (r+1, c)
                weight = m[r+1][c]
                graph.add_edge(u, v, weight)
    # also add a start element and create an edge to first val
    graph.add_edge('START', (0,0), m[0][0])
    return graph, 'START', (ROWS-1, COLS-1)

def ANSWER():
    graph, start, end = load_file('matrix.txt')
    print('Start:', start, 'End:', end)
    path = euler.utils.graph.dijkstra(graph, start, end)
    path_cost = euler.utils.graph.path_cost(graph, path)
    return path_cost

def TEST():
    expect = [131, 201, 96, 342, 746, 422, 121, 37, 331]
    graph, start, end = load_file('matrix_test.txt')
    actual = euler.utils.graph.dijkstra(graph, start, end)
    actual_cost = euler.utils.graph.path_cost(graph, actual)
    print('ACTUAL:', actual, '=', actual_cost)
    print('EXPECT:', expect, '=', sum(expect))

if __name__ == '__main__':
    import euler.utils
    euler.utils.solution_printer(ANSWER)



