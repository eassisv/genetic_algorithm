import sys
from random import choice, random
import networkx as nx
import matplotlib.pyplot as plt
from pyeasyga import pyeasyga as pyga

colors = []


def create_individual(G):
    H = nx.Graph()
    H.add_nodes_from(
        [(u, {'color': choice(colors)}) for u in G.nodes])
    H.add_edges_from(G.edges)
    return H


def fitness_function(individual, G):
    used_colors = len(set([u['color'] for u in individual.nodes.values()]))
    fitness = 4 * used_colors
    for u, v in individual.edges:
        if individual.nodes[u]['color'] == individual.nodes[v]['color']:
            fitness += 5
    return fitness


def selection_function(population):
    return choice(population[:len(population) * 10 // 100])


def crossover_function(p1, p2):
    c1 = nx.Graph()
    c2 = nx.Graph()
    for u, v in p1.edges:
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
    color_count = []
    for color in colors:
        color_count.append((color,
                            list(individual.nodes.values()).count({'color': color})))
    color_count = list(filter(lambda x: x[1] != 0, sorted(
        color_count, key=lambda item: item[1])))
    if len(color_count) > 1:
        less_common_color = color_count[0][0]
        second_less_common_color = color_count[1][0]
        for u in individual.nodes.values():
            if u['color'] == less_common_color:
                u['color'] = second_less_common_color


def initialize_ga(graph, generations):
    ga = pyga.GeneticAlgorithm(
        graph, generations=generations, mutation_probability=0.40, elitism=True, maximise_fitness=False)
    ga.create_individual = create_individual
    ga.fitness_function = fitness_function
    ga.crossover_function = crossover_function
    ga.mutate_function = mutate_function
    ga.selection_function = selection_function
    return ga


def initialize_colors(nodes):
    for i in range(nodes):
        color = '#' + str(hex(int('ffff00', base=16) // nodes * i))[2:]
        colors.append('{:0<7}'.format(color))


def draw_graphs(initial_graph, final_graph):
    layout = nx.kamada_kawai_layout(initial_graph)
    plt.subplot(121)
    nx.draw_networkx(final_graph, pos=layout, node_color=[
                     u['color'] for u in result.nodes.values()])
    plt.subplot(122)
    nx.draw_networkx(initial_graph, pos=layout)
    plt.show()


if __name__ == '__main__':
    try:
        nodes = int(sys.argv[1])
        edge_creation_prob = float(sys.argv[2]) / 100
        generations = int(sys.argv[3])
    except:
        print('O programa precisa de 3 argumentos, leia o README para entender melhor')
        sys.exit(0)
    graph = nx.connected_watts_strogatz_graph(
        nodes, nodes // 4, edge_creation_prob)
    initialize_colors(nodes)
    ga = initialize_ga(graph, generations)
    ga.run()
    result = ga.best_individual()[1]
    draw_graphs(graph, result)
