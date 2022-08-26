# import kirchhoff.circuit_init as ki
import electricalpy

from CrGraph import *
import json
import networkx as nx
import itertools
import numpy.random as rnd
import matplotlib.pyplot as plt

NODES = []
CONNECTIONS = []
def load_the_connections_on_map():
    try:
        with open("connections.txt", 'r') as file:
            global CONNECTIONS
            # print(file.read()
            CONNECTIONS = [Connection(Node(), Node()).set_data(data, NODES) for data in json.load(file)]
            print(CONNECTIONS)
        print("CONNECTIONS LEN: " + str(len(CONNECTIONS)))
    except:
        print("НЕТ НАЧАЛЬНЫХ СОЕДИНЕНИЙ")

def load_the_points_on_map():
    try:
        with open("graph.txt", 'r') as file:
            global NODES
            NODES = [Node().set_data(data) for data in json.load(file)]
            print(NODES)
        print("NODES LEN: " + str(len(NODES)))
    except:
        print("НЕТ НАЧАЛЬНЫХ ТОЧЕК")

load_the_points_on_map()
load_the_connections_on_map()

graph = nx.Graph()
for node in NODES:
    graph.add_node(node.data)
for connection in CONNECTIONS:
    graph.add_edge(connection.node1.data, connection.node2.data, length=connection.get_length(), conductivity=connection.get_length())
print(graph.nodes())

# nx.draw_circular(graph,
#          node_color='red',
#          node_size=1000,
#          with_labels=True)
# plt.show()


# n=3
# G=nx.grid_graph(( n,n,1))
# K = ki.initialize_circuit_from_crystal(graph)

# import kirchhoff.circuit_dual as kid
# kid.initialize_dual_flux_circuit_from_minsurf('simple',3)
import kirchhoff.circuit_init as ki
from kirchhoff.circuit_flow import FlowCircuit
n=3
G=nx.grid_graph(( n,n,1))
K = ki.initialize_circuit_from_crystal("default")
# K.default_init(graph
# K.set_info(graph)
# K.
C=FlowCircuit(graph)
C.edges["conductivity"]=[k[2]["conductivity"] for k in graph.edges.data()]
C.nodes["potential"]=[i for i in range(6)]
print(C.nodes)

# C.set_source_attributes()
# C.
fig = C.plot_circuit()

print(C.edges)
fig.show()