class Graph(object):

    # constructure
    def __init__(self, graph_dict=None):
        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):
        return list(self.__graph_dict.keys())

    def edges(self):
        return self.__generate_edges()

    def __generate_edges(self):
        edges = []
        # read more about set --> thisset = {"apple", "banana", "cherry"}
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        graph = self.__graph_dict
        path = path + [start_vertex]

        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths


    def diameter(self):
        v = self.vertices()
        # all coordinated
        # [ function(i,j) for i,j in object ]
        pairs = [(v[i], v[j]) for i in range(len(v) - 1) for j in range(i + 1, len(v))]
        print "all coordinate= ", pairs
        smallest_paths = []
        # Iteration in pairs
        for (s, e) in pairs:
            paths = self.find_all_paths(s, e)
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)

        smallest_paths.sort(key=len)

        diameter = len(smallest_paths[-1]) - 1
        return diameter

if __name__ == "__main__":
    g = { "a" : ["c"],
          "b" : ["c","e","f"],
          "c" : ["a","b","d","e"],
          "d" : ["c"],
          "e" : ["b","c","f"],
          "f" : ["b","e"]
    }

    print g

    graph = Graph(g)

    print "Vertices of graph:"
    print graph.vertices()

    print "Edges of graph:"
    print graph.edges()

    print "All path from a to f:"
    print graph.find_all_paths("a", "f")


