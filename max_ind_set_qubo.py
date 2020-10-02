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

# import sys to enable entry of params when running program
import sys
# TODO update code to allow for entry of lagrange and chain_strength params

def get_token():
    '''Return your personal access token'''
    
    # TODO add secure way of including token
    return token

def create_graph(edges):
    # Create empty graph
    G = nx.Graph()

    # Add edges to graph - this also adds the nodes
    G.add_edges_from(edges)

    return G

def get_qubo(S, gamma, edges):
    """Returns a dictionary representing a QUBO.

    Args:
        S(list of integers): the value for each box
    """
    # Q = {(1, 2): 3.0, (0, 2): 3.0, (1, 3): 3.0, (2, 3): 3.0, (0, 0): -1.0, (1, 1): -1.0, (2, 2): -1.0, (3, 3): -1.0}
    Q = {}
    for i in range(len(S)):
        for j in range(len(S)):
            if j > i and (i, j) in edges:
                Q[(i, j)] = gamma
            elif j < i:
                Q[(i, j)] = 0
            else: 
                Q[(i, i)] = -1
    
    # Print qubo in matrix form
    # for i in range(len(S)):
    #     my_line = ''
    #     for j in range(len(S)):
    #         if (i,j) in Q:
    #             my_line += '\t' + str(Q[(i,j)])
    #         else:
    #             my_line += '\t' + str(0)
    #     print(my_line)

    # print(Q)
    return Q

def run_on_qpu(Q, sampler, chainstrength=1, numruns=10):
    """Runs the QUBO problem Q on the sampler provided.

    Args:
        Q(dict): a representation of a QUBO
        sampler(dimod.Sampler): a sampler that uses the QPU
    """
    sample_set = sampler.sample_qubo(Q, chain_strength=chainstrength, num_reads=numruns)

    return sample_set

## ------- Main program -------
if __name__ == "__main__":

    S = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    edges = [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (4, 5), (4, 6), (5, 6), (5, 7), (6, 8), (7,8)]
    # S = [0, 1, 2, 3]
    # edges = [(0, 1), (0, 2), (1, 3), (2, 3)]    
    
    gamma = 3
    
    token = get_token()
    G = create_graph(edges)
    Q = get_qubo(S, gamma, edges)

    chainstrength = 1 # update
    numruns = 100 # update

    # Define the sampler and run the problem
    sampler = EmbeddingComposite(DWaveSampler(endpoint='https://cloud.dwavesys.com/sapi/', token=token, solver={'qpu': True}))
    sample_set = run_on_qpu(Q, sampler, chainstrength, numruns)

    # Print the solution
    print('Maximum independent set size found is', sum(sample_set.first.sample.values()))
    print(sample_set.first)

    # # Visualize the results
    # subset_1 = G.subgraph(S)
    # notS = list(set(G.nodes()) - set(S))
    # subset_0 = G.subgraph(notS)
    # pos = nx.spring_layout(G)
    # plt.figure()

    # # Save original problem graph
    # original_name = "antenna_plot_original.png"
    # nx.draw_networkx(G, pos=pos, with_labels=True)
    # plt.savefig(original_name, bbox_inches='tight')

    # # Save solution graph
    # # Note: red nodes are in the set, blue nodes are not
    # solution_name = "antenna_plot_solution.png"
    # nx.draw_networkx(subset_1, pos=pos, with_labels=True, node_color='r', font_color='k')
    # nx.draw_networkx(subset_0, pos=pos, with_labels=True, node_color='b', font_color='w')
    # plt.savefig(solution_name, bbox_inches='tight')

    # print("Your plots are saved to {} and {}".format(original_name, solution_name))
