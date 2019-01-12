""" Problem 81

NOTE: This problem is a more challenging version of Problem 81.

The minimal path sum in the 5 by 5 matrix below, by starting in any cell in the
left column and finishing in any cell in the right column, and only moving up,
down, and right, is indicated in red and bold; the sum is equal to 994.

    131  673  234--103--013
               |
    201--096--342  965  150

    630  803  746  422  111

    537  699  497  121  956

    805  732  524  037  311

Find the minimal path sum in the 80 by 80 matrix, from the left column to the
right column."""

from __future__ import print_function
import euler.utils.graph

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
    graph = euler.utils.graph.DiGraph()
    ROWS = len(m)
    COLS = len(m[0])
    for r in range(ROWS):
        for c in range(COLS):
            u = (r, c)
            # Add add to node to the right
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
    # also add a start element and create edges to first column
    start_node = 'START'
    for row in range(ROWS):
        node = (row, 0)
        weight = m[row][0]
        graph.add_edge(start_node, node, weight)
    # also add an end element and create edges to the list column
    end_node = 'END'
    c = COLS-1
    for row in range(ROWS):
        node = (row, c)
        weight = 0 # Valid?
        graph.add_edge(node, end_node, weight)
    return graph, start_node, end_node

def ANSWER():
    graph, start, end = load_file('matrix.txt')
    path = euler.utils.graph.dijkstra(graph, start, end)
    path_cost = euler.utils.graph.path_cost(graph, path)
    return path_cost

def TEST():
    expect = [201, 96, 342, 234, 103, 18]
    graph, start, end = load_file('matrix_test.txt')
    actual = euler.utils.graph.dijkstra(graph, start, end)
    actual_cost = euler.utils.graph.path_cost(graph, actual)
    print('ACTUAL:', actual, '=', actual_cost)
    print('EXPECT:', expect, '=', sum(expect))

if __name__ == '__main__':
    import euler.utils
    #TEST()
    euler.utils.solution_printer(ANSWER)



