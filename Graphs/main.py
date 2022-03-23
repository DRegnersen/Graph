import datetime
import networkx as nx
import matplotlib.pyplot as plt

settings = {}

file = open("settings.txt", mode="r")
for line in file:
    args = line.split()
    if len(args) >= 2 and args[0] == "graph" and args[1] == "+=":
        for parameter in args[2:]:
            if parameter not in settings:
                settings[parameter] = 1


def donetsk_edition():
    graph.add_edge("Russia", "Luhansk People's Republic")
    graph.add_edge("Russia", "Donetsk People's Republic")
    graph.add_edge("Ukraine", "Luhansk People's Republic")
    graph.add_edge("Ukraine", "Donetsk People's Republic")
    graph.add_edge("Luhansk People's Republic", "Donetsk People's Republic")


graph = nx.read_adjlist("neighbours_of_europe.txt", delimiter=",")

if "donetsk_edition" in settings:
    donetsk_edition()

plt.figure(figsize=(17, 15))

nx.draw_planar(graph, with_labels=True, node_color="#cfc8f9", edge_color="#6a5acd")

if "file" in settings:
    current_time = str(datetime.datetime.now())[:-7].replace(":", ".")

    plt.savefig("countries_of_europe\\EU " + current_time + ".png")
    print("File 'EU " + current_time + ".png' was successfully created")

if "info" in settings:
    print("=== INFO ===")

    graph_cc = sorted(nx.connected_components(graph), key=len, reverse=True)
    max_subgraph = graph.subgraph(graph_cc[0])

    print("Number of nodes:", max_subgraph.number_of_nodes())
    print("Number of edges:", max_subgraph.number_of_edges())

    min_degree = -1
    max_degree = 0

    for vertex in max_subgraph.nodes:
        min_degree = max_subgraph.degree(vertex) if min_degree < 0 else min(max_subgraph.degree(vertex), min_degree)
        max_degree = max(max_subgraph.degree(vertex), max_degree)

    print("Minimal degree:", min_degree)
    print("Maximal degree:", max_degree)
    print("Radius:", nx.radius(max_subgraph))
    print("Diameter:", nx.diameter(max_subgraph))
    print("Girth:", min(nx.cycle_basis(max_subgraph), key=len))
    print("Centers:", nx.center(max_subgraph))
    print("Vertex Connectivity:", nx.node_connectivity(max_subgraph))
    print("Edge Connectivity:", nx.edge_connectivity(max_subgraph))

    cur_strategy = "saturation_largest_first"
    print("Vertex coloring:", nx.greedy_color(max_subgraph, strategy=cur_strategy))
    print("(Number of vertexes' colors:", max(nx.greedy_color(max_subgraph, strategy=cur_strategy).values()) + 1, ")")

    min_coloring = {}

    for vertex in max_subgraph.nodes():
        coloring = {}

        for edge in nx.bfs_edges(graph, vertex):
            if edge[::-1] not in coloring:
                used_colors = []

                for begin in graph.edges(edge[0]):
                    if begin in coloring:
                        used_colors.append(coloring[begin])
                    elif begin[::-1] in coloring:
                        used_colors.append(coloring[begin[::-1]])

                for end in graph.edges(edge[1]):
                    if end in coloring:
                        used_colors.append(coloring[end])
                    elif end[::-1] in coloring:
                        used_colors.append(coloring[end[::-1]])

                current_color = 0
                while current_color in used_colors:
                    current_color += 1

                coloring[edge] = current_color

        if len(min_coloring) == 0:
            min_coloring = coloring
        elif len(coloring) != 0 and max(coloring.values()) < max(min_coloring.values()):
            min_coloring = coloring

    print("Edge coloring:", min_coloring)
    print("(Number of edges' colors:", max(min_coloring.values()) + 1, ")")

    print("Maximum clique:", nx.approximation.max_clique(max_subgraph))
    print("Maximum stable set:", nx.approximation.maximum_independent_set(max_subgraph))
    print("Maximum matching:", nx.maximal_matching(max_subgraph))

    print("Minimum vertex cover:", nx.approximation.min_weighted_vertex_cover(max_subgraph))
    print("(Number of vertexes in covering:", len(nx.approximation.min_weighted_vertex_cover(max_subgraph)), ")")

    print("Minimum edge cover:", nx.min_edge_cover(max_subgraph))
    print("(Number of edges in covering:", len(nx.min_edge_cover(max_subgraph)), ")")
    print("Shortest closed walk visiting every vertex:", nx.approximation.traveling_salesman_problem(max_subgraph))

    eulerian_graph = nx.eulerize(max_subgraph)
    shortest_eulerian = []

    for begin in eulerian_graph.nodes():
        current_circuit = list(nx.eulerian_circuit(eulerian_graph, source=begin))

        if not shortest_eulerian or len(shortest_eulerian) > len(current_circuit):
            shortest_eulerian = current_circuit

    print("Shortest closed walk visiting every edge:", shortest_eulerian)

blocks = list(nx.biconnected_components(graph))
block_cut_graph = nx.Graph()

for node in range(0, len(blocks)):
    block_cut_graph.add_node(node)

for begin in range(0, len(blocks)):
    for current in blocks[begin]:
        for end in range(0, len(blocks)):
            if begin != end and current in blocks[end]:
                block_cut_graph.add_edge(begin, end)

if "block_cut" in settings:
    plt.close()
    nx.draw_planar(block_cut_graph, with_labels=False, node_color="#00ff7f", edge_color="#00cc7a")
    current_time = str(datetime.datetime.now())[:-7].replace(":", ".")

    plt.savefig("block_cut\\BC " + current_time + ".png")
    print("File 'BC " + current_time + ".png' was successfully created")

if "info" in settings:
    print("Blocks:", blocks)
    print("2-edge-connected components:", list(nx.k_edge_components(graph, 2)))