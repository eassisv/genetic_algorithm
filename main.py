import sys
from random import choice
import networkx as nx
import matplotlib.pyplot as plt
from pyeasyga import pyeasyga as pyga

colors = [
    '#ff0000',
    '#00ff00',
    '#0000ff',
    '#aaaaaa',
    '#ffaaaa',
    '#aaffaa',
    '#aaaaff',
    '#444444',
    '#ff4444',
    '#44ff44',
    '#4444ff'
]


def create_individual(G):
    H = nx.Graph()
    H.add_nodes_from(
        [(u, {'color': choice(colors)}) for u in G.nodes])
    H.add_edges_from(G.edges)
    return H


def fitness_function(individual, G):
    used_colors = len(set([u['color'] for u in individual.nodes.values()]))
    fitness = 7 * used_colors
    for u, v in individual.edges:
        if individual.nodes[u]['color'] == individual.nodes[v]['color']:
            fitness += 2
    return fitness


def selection_function(population):
    return choice(population[:len(population) * 10 // 100])


def crossover_function(p1, p2):
    c1 = nx.Graph()
    c2 = nx.Graph()
    for u, v in p1.edges():
        if p1.nodes[u]['color'] == p1.nodes[v]['color']:
            c1.add_node(u, color=p2.nodes[u]['color'])
            c1.add_node(v, color=p2.nodes[v]['color'])
        else:
            c1.add_node(u, color=p1.nodes[u]['color'])
            c1.add_node(v, color=p1.nodes[v]['color'])
        c1.add_edge(u, v)
    for u, v in p2.edges():
        if p2.nodes[u]['color'] == p2.nodes[v]['color']:
            c2.add_node(u, color=p1.nodes[u]['color'])
            c2.add_node(v, color=p1.nodes[v]['color'])
        else:
            c2.add_node(u, color=p2.nodes[u]['color'])
            c2.add_node(v, color=p2.nodes[v]['color'])
        c2.add_edge(u, v)
    return c1, c2


def mutate_function(individual):
    for u, v in individual.edges:
        if individual.nodes[u]['color'] == individual.nodes[v]['color']:
            individual.nodes[u]['color'] = choice(colors)


def initialize_ga(graph):
    ga = pyga.GeneticAlgorithm(
        graph, generations=10000, elitism=True, maximise_fitness=False)
    ga.create_individual = create_individual
    ga.fitness_function = fitness_function
    ga.crossover_function = crossover_function
    ga.mutate_function = mutate_function
    ga.selection_function = selection_function
    return ga


if __name__ == '__main__':
    nodes = int(sys.argv[1])
    edge_creation_prob = float(sys.argv[2]) / 100

    graph = nx.connected_watts_strogatz_graph(
        nodes, nodes // 2, edge_creation_prob)
    ga = initialize_ga(graph)
    ga.run()
    result = ga.best_individual()[1]
    print(result.nodes)
    print(result.edges)
    plt.subplot(111)
    nx.draw_networkx(result, node_color=[u['color']
                                         for u in result.nodes.values()])
    plt.show()
