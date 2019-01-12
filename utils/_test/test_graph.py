from euler.utils import graph
import unittest

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.g = graph.Graph()

    def test_constructed_empty(self):
        self.assertEqual(0, len(self.g))
        
    def test_add_node(self):
        self.g.add_node(1)
        self.assertIn(1, self.g)

    def test_len(self):
        self.g.add_node(1)
        self.assertEqual(1, len(self.g))

    def test_add_nodes(self):
        self.g.add_nodes([1,2,3])
        self.assertEqual(3, len(self.g))
        self.assertIn(1, self.g)
        self.assertIn(2, self.g)
        self.assertIn(3, self.g)

    def test__getitem__(self):
        self.g.add_nodes([1,2])
        self.assertEqual(self.g[1], {})
        self.assertEqual(self.g[2], {})
        self.g.add_edge(1, 2)
        self.assertIn(2, self.g[1])
        self.assertIn(1, self.g[2])
    
    def test_edge_iter_does_not_duplicate(self):
        self.g.add_edge(1, 2)
        edges = self.g.edge_list()
        self.assertTrue(not ((1,2) in edges and (2,1) in edges))

    def test_add_edge_weight(self):
        self.g.add_node(1)
        self.g.add_node(2)
        self.g.add_edge(1, 2, 6)
        self.assertIn(2, self.g[1])

    def test_add_edge_adds_nodes(self):
        self.g.add_edge(1, 2)
        self.assertEqual(2, len(self.g))
        self.assertIn(1, self.g)
        self.assertIn(2, self.g)
        edges = self.g.edge_list()
        self.assertTrue((1,2) in edges or (2,1) in edges)

    def test_add_edge_adds_nodes_with_weights(self):
        self.g.add_edge(1, 2, 54)
        self.assertEqual(2, len(self.g))
        self.assertIn(1, self.g)
        self.assertIn(2, self.g)
        edges = self.g.edge_list(weights=True)
        self.assertTrue((1,2, 54) in edges or (2,1, 54) in edges)
        self.assertEqual(self.g[1][2], 54)
        self.assertEqual(self.g[2][1], 54)

    def test_neighbors(self):
        self.g.add_node(1)
        self.assertEqual([], self.g.neighbors(1))
        self.g.add_edge(1, 2)
        self.assertEqual([2], self.g.neighbors(1))
        self.assertEqual([1], self.g.neighbors(2))


class TestDiGraph(unittest.TestCase):

    def setUp(self):
        self.g = graph.DiGraph()

    def test_constructed_empty(self):
        self.assertEqual(0, len(self.g))
        
    def test_add_node(self):
        self.g.add_node(1)
        self.assertIn(1, self.g)

    def test_len(self):
        self.g.add_node(1)
        self.assertEqual(1, len(self.g))

    def test_add_nodes(self):
        self.g.add_nodes([1,2,3])
        self.assertEqual(3, len(self.g))
        self.assertIn(1, self.g)
        self.assertIn(2, self.g)
        self.assertIn(3, self.g)

    def test__getitem__(self):
        self.g.add_nodes([1,2])
        self.assertEqual(self.g[1], {})
        self.assertEqual(self.g[2], {})
        self.g.add_edge(1, 2)
        self.assertIn(2, self.g[1])
    
    def test_edge_iter_does_not_duplicate(self):
        self.g.add_edge(1, 2)
        self.g.add_edge(2, 3)
        self.g.add_edge(1, 3)
        self.assertIn((1,2), self.g.edge_list())
        self.assertIn((2,3), self.g.edge_list())
        self.assertIn((1,3), self.g.edge_list())

    def test_add_edge_weight(self):
        self.g.add_node(1)
        self.g.add_node(2)
        self.g.add_edge(1, 2, 6)
        self.assertIn(2, self.g[1])

    def test_add_edge_adds_nodes(self):
        self.g.add_edge(1, 2)
        self.assertEqual(2, len(self.g))
        self.assertIn(1, self.g)
        self.assertIn(2, self.g)
        self.assertIn((1,2), self.g.edge_list())

    def test_add_edge_adds_nodes_with_weights(self):
        self.g.add_edge(1, 2, 54)
        self.assertEqual(2, len(self.g))
        self.assertIn(1, self.g)
        self.assertIn(2, self.g)
        self.assertEqual([(1, 2, 54)], self.g.edge_list(weights=True))
        self.assertEqual(self.g[1][2], 54)

    def test_neighbors(self):
        self.g.add_node(1)
        self.assertEqual([], self.g.neighbors(1))
        self.g.add_edge(1, 2)
        self.assertEqual([2], self.g.neighbors(1))


class TestAlgorithmsDigraph(unittest.TestCase):

    def create_digraph(self):
        m = [[131, 673, 234, 103,  18],
             [201,  96, 342, 965, 150],
             [630, 803, 746, 422, 111],
             [537, 699, 497, 121, 956],
             [805, 732, 524,  37, 331]]
        g = graph.DiGraph()
        ROWS = len(m)
        COLS = len(m[0])
        for r in range(ROWS):
            for c in range(COLS):
                u = m[r][c]
                if c+1 < COLS:
                    v = m[r][c+1]
                    g.add_edge(u, v, v)
                if r+1 < ROWS:
                    v = m[r+1][c]
                    g.add_edge(u, v, v)
        return g
        
    def test_dijkstra_digraph(self):
        expect = [131, 201, 96, 342, 746, 422, 121, 37, 331]
        g = self.create_digraph()
        actual = graph.dijkstra(g, 131, 331)
        self.assertEqual(expect, actual)
        
if __name__ == '__main__':
    unittest.main(verbosity=2, exit=False)
