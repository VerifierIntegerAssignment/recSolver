""" 
A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
Basic Code Taken from http://www.python-course.eu/graphs_python.php
"""


class Graph(object):
    
    cycles=[]
    edge_list=[]

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res
    
    def cyclic(self):
        """Add by pritom 12/06/2017

        """
        path = set()

        def visit(vertex):
            path.add(vertex)
            for neighbour in self.__graph_dict.get(vertex, ()):
                if neighbour in path or visit(neighbour):
                    return True
            path.remove(vertex)
            return False

        return any(visit(v) for v in self.__graph_dict)

    def find_path(self, start_vertex, end_vertex, path=None):
        """ find a path from start_vertex to end_vertex 
            in graph """
        if path == None:
            path = []
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, 
                                               end_vertex, 
                                               path)
                if extended_path: 
                    return extended_path
        return None
    
    
    def getAllNodesInCycle(self):
        self.cycles=[]
        self.edge_list=self.set2List()              
        for edge in self.edge_list:
            for node in edge:
                self.findNewCycles([node])
        self.detectLoop()
        return self.cycles
    
    
    
    def findNewCycles(self, path):
        start_node = path[0]
        next_node= None
        sub = []
        #visit each edge and each node of each edge
        for edge in self.edge_list:
            node1, node2 = edge
            if start_node in edge:
                    if node1 == start_node:
                        next_node = node2
                    else:
                        next_node = node1
            if not self.visited(next_node, path):
                    # neighbor node not on path yet
                    sub = [next_node]
                    sub.extend(path)
                    # explore extended path
                    self.findNewCycles(sub);
            elif len(path) > 2  and next_node == path[-1]:
                    # cycle found
                    p = self.rotate_to_smallest(path);
                    inv = self.invert(p)
                    if self.isNew(p) and self.isNew(inv):
                        self.cycles.append(p)
            elif len(path) == 2  and next_node == path[-1]:
                    p = self.rotate_to_smallest(path);
                    inv = self.invert(p)
                    if self.isNew(p) and self.isNew(inv) and self.checkSmall(p[0],p[1]):
                         self.cycles.append(p)

    def invert(self,path):
        return self.rotate_to_smallest(path[::-1])

    #  rotate cycle path such that it begins with the smallest node
    def rotate_to_smallest(self,path):
        n = path.index(min(path))
        return path[n:]+path[:n]

    def isNew(self,path):
        return not path in self.cycles

    def visited(self,node, path):
        return node in path
    
    def checkSmall(self,node1,node2):
        edges1=self.__graph_dict[node1]
        edges2=self.__graph_dict[node2]
        if node1 in edges2 and node2 in edges1:
            return True
        return False
    
    def set2List(self):
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                #if {neighbour, vertex} not in edges:
                temp_edges=[]
                temp_edges.append(vertex)
                temp_edges.append(neighbour)
                edges.append(temp_edges)
        return edges
    
    def detectLoop(self):
        for vertex in self.__graph_dict:
            if vertex in self.__graph_dict[vertex]:
                self.cycles.append([vertex])