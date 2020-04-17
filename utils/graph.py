class Graph:
    """
    graph = {'State A': [('State B', func1), ('State C', func2)],
             'State B': [('State C', func3)],
             'State C': []}
    """
    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if(not self.has_node(node)):
            self.graph[node] = []

    def add_edge(self, start_node, end_node, weight):
        self.graph[start_node] += [(end_node, weight)]

    def has_node(self, node):
        return node in self.graph.keys()

    def __repr__(self):
        return self.graph