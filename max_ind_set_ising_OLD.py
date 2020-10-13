# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

## ------- import packages -------
# Import networkx for graph tools
import networkx as nx

# Import dwave_networkx for d-wave graph tools/functions
import dwave_networkx as dnx

# Import dwave.system packages for the QPU
from dwave.system import DWaveSampler, EmbeddingComposite

# Import matplotlib.pyplot to draw graphs on screen
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

def create_graph(edges):
    """Returns a graph based on the specified list of edges.

    Args:
        edges(list of tuples): each tuple represents an edge in the graph
    """
    # Create empty graph
    G = nx.Graph()

    # Add edges to graph - this also adds the nodes
    G.add_edges_from(edges)

    return G

def get_ising(nodes, edges):
    """Returns a dictionary representing the Ising formulation.

    Args:
        nodes(list of integers): nodes for the graph
        edges(list of tuples): each tuple represents an edge in the graph
    """
    # Set gamma
    gamma = 3
    
    # Create Ising
    h = {}
    J = {}

    min_node = min(nodes)
    edge_dict = dict.fromkeys(nodes, 0)

    # TODO - Fix this code to generate the Ising representation correctly
    for u, v in G.edges:
        J[(u, v)] = 0.25*gamma
        edge_dict[u] += 1
        edge_dict[v] += 1
    for n in G.nodes:
        h[(min_node, n)] = (0.75*edge_dict[n] - 0.5)
    
    print(h)
    print(J)
    return h, J

def run_on_qpu(h, J, sampler, chainstrength, num_reads):
    """Runs the Ising problem on the sampler provided.

    Args:
        h(dict): a representation of the linear terms of the ising problem
        J(dict): a representation of the quadratic terms of the ising problem
        sampler(dimod.Sampler): a sampler that uses the QPU
    """
    sample_set = sampler.sample_ising(h, J, chain_strength=chainstrength, num_reads=num_reads)

    return sample_set

## ------- Main program -------
if __name__ == "__main__":

    # Test Graph 0 (solution = 2)
    nodes = [0, 1, 2]
    edges = [(0, 1), (1, 2)]

    # # Test Graph 1 (solution = 2)
    # nodes = [0, 1, 2, 3, 4]
    # edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]

    # # Test Graph 2 (solution = 5)
    # nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 6), (5, 6), (5, 7), (6, 8), (7, 8)]

    # # Test Graph 3 (solution = 5)
    # nodes = [0, 1, 2, 3, 4, 5, 6, 7]
    # edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (3, 6), (4, 7), (6, 7)]

    # # Test Graph 4 (solution = 9)
    # nodes = list(i for i in range(24))
    # edges = [(12, 16), (12, 20), (13, 17), (13, 21), (14, 18), (14, 22), (15, 19), (15, 23), (16, 20),
    #  (16, 12), (17, 21), (17, 13), (18, 22), (18, 14), (19, 23), (19, 15), (20, 12), (20, 16), (21, 13),
    #  (21, 17), (22, 14), (22, 18), (23, 15), (23, 19), (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), 
    #  (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (0, 11), (0, 12), (1, 13), (2, 14), (3, 15), (4, 16), 
    #  (5, 17), (6, 18), (7, 19), (8, 20), (9, 21), (10, 22), (11, 23)]
    
    # Create graph
    G = create_graph(edges)

    # Get Ising formulation
    h, J = get_ising(nodes, edges)

    # Set chainstrength and num_reads
    chainstrength = 1 # update
    num_reads = 100 # update

    # Define the sampler and run the problem
    sampler = EmbeddingComposite(DWaveSampler(endpoint='https://cloud.dwavesys.com/sapi/', solver={'qpu': True}))
    sample_set = run_on_qpu(h, J, sampler, chainstrength, num_reads)

    # Print the solution
    print(sample_set)    
    spinResult = list(sample_set.first.sample[i] for i in nodes)
    vertices = []
    for i in range(len(spinResult)):
        if spinResult[i] == 1:
            vertices.append(i)
    print('Maximum independent set size found is', (len(vertices)))
    print(vertices)

    # Visualize the results
    subset_1 = G.subgraph(vertices)
    notVertices = list(set(G.nodes()) - set(vertices))
    subset_0 = G.subgraph(notVertices)
    pos = nx.spring_layout(G)
    plt.figure()

    # Save original problem graph
    original_name = "graph_original.png"
    nx.draw_networkx(G, pos=pos, with_labels=True)
    plt.savefig(original_name, bbox_inches='tight')

    # Save solution graph
    # Note: red nodes are in the set, blue nodes are not
    solution_name = "graph_solution.png"
    nx.draw_networkx(subset_1, pos=pos, with_labels=True, node_color='r', font_color='k')
    nx.draw_networkx(subset_0, pos=pos, with_labels=True, node_color='b', font_color='w')
    plt.savefig(solution_name, bbox_inches='tight')

    print("Your plots are saved to {} and {}".format(original_name, solution_name))