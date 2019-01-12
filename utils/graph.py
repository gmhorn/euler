from __future__ import print_function
import heapq

def path_cost(graph, path):
    path_weights = []
    for i in range(len(path)-1):
        e1, e2 = path[i], path[i+1]
        path_weights.append(graph[e1][e2])
    return sum(path_weights)
            

def dijkstra(graph, start, goal):
    opened = [(0, start, None)]
    closed = {}
    explored = {}
    while opened:
        dist, curr_node, parent = heapq.heappop(opened)
        if curr_node == goal:
            path = [curr_node]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path
        if curr_node in explored:
            continue
        explored[curr_node] = parent
        for neighbor in graph[curr_node]:
            if neighbor in explored:
                continue
            new_cost = dist + graph[curr_node][neighbor]
            if neighbor in closed:
                old_cost = closed[neighbor]
                if old_cost <= new_cost:
                    continue
            closed[neighbor] = new_cost
            heapq.heappush(opened, (new_cost, neighbor, curr_node))
    raise Exception('Node %s not reachable from %s' % (start, goal))
                
class Graph(object):
    """ Base class for undirected graph.

    Allows any hashable object as node. Can add weight to each edge. """
    def __init__(self):
        self._adj = dict() # Adjacency dict
        self._nodes = set() # Node set

    def __iter__(self):
        """ Iterator over the nodes of graph. """
        return iter(self._nodes)

    def __len__(self):
        """ Returns number of nodes """
        return len(self._nodes)

    def __getitem__(self, n):
        """ Returns a dict of neighbors of node n. """
        return self._adj[n]

    def add_node(self, node):
        if node in self._nodes:
            raise Exception('Node %s already exists in graph!' % n)
        self._nodes.add(node)
        self._adj[node] = {}

    def add_nodes(self, nodes):
        for node in nodes:
            self.add_node(node)

    def add_edge(self, u, v, weight=None):
        """ Adds an undirected edge from u <-> v, with an optional weight. """
        if u not in self._nodes:
            self.add_node(u)
        if v not in self._nodes:
            self.add_node(v)
        self._adj[u][v] = weight
        self._adj[v][u] = weight

    def neighbors(self, n):
        """ Returns list of neighbors of node n. """
        return list(self._adj[n])

    def edges(self, weights=False):
        """ Returns iterator for edges. """
        seen = {}
        for node, neighbors in self._adj.iteritems():
            for neighbor, weight in neighbors.iteritems():
                if  neighbor not in seen:
                    if weights:
                        yield (node, neighbor, weight)
                    else:
                        yield (node, neighbor)
            seen[node] = 1
        del seen

    def edge_list(self, weights=False):
        return list(self.edges(weights))


class DiGraph(Graph):
    """ Base class for directed graph.

    Allows any hashable object as node. Can add weight to each edge. """
    def __init__(self):
        self._nodes = set() # Node set
        self._pred = dict() # Predecessor dict
        self._succ = dict()# Successor dict
        self._adj = self._succ # Successor = adjacency dict

    def add_node(self, node):
        super(DiGraph, self).add_node(node)
        self._pred[node] = {}

    def add_edge(self, u, v, weight=None):
        """ Adds a directed edge from u -> v, with an optional weight. """
        if u not in self._nodes:
            self.add_node(u)
        if v not in self._nodes:
            self.add_node(v)
        self._succ[u][v] = weight
        self._pred[v][u] = weight

    def successors(self, n):
        return iter(self._succ[n])

    def predecessors(self, n):
        return iter(self._pred[n])

    def edges(self, weights=False):
        """ Returns iterator for edges. """
        for node, neighbors in self._adj.iteritems():
            for neighbor, weight in neighbors.iteritems():
                if weights: yield (node, neighbor, weight)
                else:       yield (node, neighbor)
