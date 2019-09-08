import random
import matplotlib.pyplot as plt
import networkx as nx

class Network(object):
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

        for vertex in self.__graph_dict:
            # print vertex
            for nei_id in range(len(self.__graph_dict[vertex]["neighbor"])):
                # print "nei=", self.__graph_dict[vertex]["neighbor"][nei_id]
                # print "cost=", self.__graph_dict[vertex]["cost"][nei_id]
                tmp_data = {
                    "data":{self.__graph_dict[vertex]["neighbor"][nei_id], vertex},
                    "cost":self.__graph_dict[vertex]["cost"][nei_id]
                }
                if tmp_data not in edges:
                    edges.append(tmp_data)
        return edges

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        graph = self.__graph_dict
        path = path + [start_vertex]

        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]["neighbor"]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def myShrotedPath(self, src, dest):
        all_path = self.find_all_paths(src, dest)
        edges = self.edges()
        # print "edges=", edges
        ospf = []
        for path in all_path:
            # print "path=", path
            cost = 0
            # calculate path cost
            for node_id in range(len(path) - 1):
                # print "pair=", path[node_id], ":", path[node_id + 1]
                bridge = {path[node_id], path[node_id + 1]}
                # print "bridge=", bridge
                for e in edges:
                    if e['data'] == bridge:
                        cost = cost + e['cost']
            # print "cost=", cost
            ospf.append({'path':path, 'cost': cost})
        # print "ospf=", ospf
        ospf_cost = 0
        # find least cost
        for i in range(len(ospf)):
            if i == 0:
                ospf_cost = ospf[i]['cost']
            else:
                if ospf[i]['cost'] < ospf_cost:
                    ospf_cost = ospf[i]['cost']
        # print "ospf_cost=", ospf_cost
        # find shortest path
        shortes_path = []
        for shortest in ospf:
            if shortest['cost'] == ospf_cost:
                shortes_path.append(shortest)
        # print "shortest_path=", shortes_path
        return shortes_path

    def find_isolated_nodes(self):
        graph = self.__graph_dict
        isolated = []
        for node in graph:
            if not graph[node]:
                isolated += node
        return isolated

    def drawing(self):
        G = nx.Graph()
        graph = self.__graph_dict
        nodes = []
        edges = self.edges()
        print "edges=", edges
        for node in graph:
            # print "node=", node
            nodes.append(node)
        # print "nodes=", nodes

        edges_list = []
        for edge in edges:
            # print edge['data']
            pair = (edge['data'].pop(), edge['data'].pop())
            edges_list.append(pair)
        # print "edges list=", edges_list
        G.add_nodes_from(nodes)
        G.add_edges_from(edges_list)
        nx.draw_networkx(G, with_labels=True)
        plt.show()

    @staticmethod
    def createTopology():
        num_node = 10
        my_graph = {}
        for i in range(num_node):
            my_graph[chr(i + ord('a'))] = {"neighbor": [], "cost": []}
        # print "empty routing table=", my_graph

        for node in my_graph:
            # node is key of my_graph
            # print "node", node, "routing table=", my_graph[node]
            connect_to_id = random.randint(0, num_node - 1)
            connect_to = chr(connect_to_id + ord('a'))
            # protect connect to itself
            # protect connect to unvailable port
            if len(my_graph[node]["neighbor"]) < 3:
                while connect_to == node or len(my_graph[connect_to]["neighbor"]) >= 3:
                    # print node, "cannot connect to", connect_to
                    connect_to_id = random.randint(0, num_node - 1)
                    connect_to = chr(connect_to_id + ord('a'))
                # print node, "connected to=", connect_to
                cost = random.randint(1, 5)
                # protect duplicated connection
                if connect_to not in my_graph[node]["neighbor"]:
                    my_graph[node]["neighbor"].append(connect_to)
                    my_graph[connect_to]["neighbor"].append(node)
                    my_graph[node]["cost"].append(cost)
                    my_graph[connect_to]["cost"].append(cost)
                # print "node(update)", node, "routing table=", my_graph[node]
        print "routing table=", my_graph
        return my_graph

if __name__ == "__main__":

    my_graph = Network.createTopology()
    graph = Network(my_graph)

    print "Vertices of graph:"
    print graph.vertices()

    print "Edges of graph:"
    print graph.edges()

    print "Isolate node:"
    print graph.find_isolated_nodes()

    src = "a"
    dest = "j"
    print "All path from" , src, "to", dest, ":"
    print graph.find_all_paths(src, dest)

    print "Shorted path from" , src, "to", dest, ":"
    print graph.myShrotedPath(src, dest)

    graph.drawing()