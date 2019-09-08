import random
import matplotlib.pyplot as plt
import networkx as nx

class Network(object):
    @staticmethod
    def pathCostMax():
        return 10
    @staticmethod
    def numNode():
        return 10
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
        # recording passed node
        path = path + [start_vertex]
        # if found destination
        if start_vertex == end_vertex:
            return [path]
        # if input start vertext not in graph
        if start_vertex not in graph:
            return []
        # if end of way but not found the destination, paths will be blank []
        paths = []
        for vertex in graph[start_vertex]["neighbor"]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex,
                                                     end_vertex,
                                                     path)
                # extended_paths will be blank if cannot reach the destination
                # append each available path to paths[]
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
        plt.figure(figsize=(12, 6))
        graph = self.__graph_dict
        nodes = self.vertices()
        edges = self.edges()

        for node in nodes:
            G.add_node(node, pos=(random.randint(1, 100), random.randint(1, 100)))

        edges_list = []
        for edge in edges:
            G.add_edge(edge['data'].pop(), edge['data'].pop(), weight=edge['cost'], label=str(edge['cost']))

        elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= Network.pathCostMax()/2]  # solid edge
        esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > Network.pathCostMax()/2]  # dashed edge

        # Retrieve the positions from graph nodes and save to a dictionary
        pos = nx.get_node_attributes(G, 'pos')

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=200, node_color='orange')
        # Draw node labels
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

        # Draw edges
        nx.draw_networkx_edges(G, pos, edgelist=elarge, width=2, edge_color='g')
        nx.draw_networkx_edges(G, pos, edgelist=esmall, arrows=False, width=3,
                               alpha=0.5, edge_color='b', style='dashed')

        # Draw edge labels
        edge_labels = dict([((u, v), d['label'])
                            for u, v, d in G.edges(data=True)])

        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        plt.axis('off')
        plt.show()

    @staticmethod
    def createTopology():
        num_node = Network.numNode()
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
                cost = random.randint(1, Network.pathCostMax())
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