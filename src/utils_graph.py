import networkx as nx
import community as community_louvain
import igraph as ig
import numpy as np

# Undirected Graph metrics
def modularity_louvain(graph):
    # Detect the best partition
    partition = community_louvain.best_partition(graph, randomize=False)
    # Calculate modularity
    modularity_score = community_louvain.modularity(partition, graph)
    return modularity_score

def modularity_macroareas(graph, macro_areas_list):
    metric = nx.community.modularity(graph, macro_areas_list)
    return metric

def graph_metrics(METRIC, graph, macro_areas_list):
    edges_full = 345*345
    if METRIC=='number_connected_components':
        metric = nx.number_connected_components(graph) # number of connected components
    elif METRIC=='size_giant_component':
        metric = len(sorted(nx.connected_components(graph), key=len, reverse=True)[0]) # size giant component
    elif METRIC=='average_shortest_path':
        GiantComponent = graph.subgraph(sorted(nx.connected_components(graph), key=len, reverse=True)[0]).copy()                    
        metric = nx.average_shortest_path_length(GiantComponent) # Average shortest path inside the giant component
    elif METRIC=='global_average_shortest_path':
        sps = [list(nx.shortest_path_length(graph.subgraph(cc).copy())) for cc in nx.connected_components(graph)]
        global_sps = []
        for sp in sps:
            for l in sp:
                global_sps += list(l[1].values())
        metric = np.mean(global_sps) # Average shortest path (global)
    elif METRIC=='fraction_of_edges':
        edges = graph.number_of_edges()
        metric = edges/edges_full # fraction of remaining edges inside the graph
    elif METRIC=='node_wih_link':
        nodes = len([n for n in graph.nodes if len(list(graph.neighbors(n))) > 0])
        metric = nodes/nodes_full # node with at least a link
    #                 centr = nx.betweenness_centrality(GiantComponent)
    #                 max_centr_key = max(centr, key=centr.get)
    #                 max_centr = centr[max_centr_key]
    #                 metric = max_centr
    #                 metric = nx.betweenness_centrality(graph)[node] # centrality of a selected node
    #             print(metric)
    elif METRIC=='degree_distribution':
        d = sorted((d for n, d in graph.degree() if d!=0), reverse=True) # degree distribution
    elif METRIC=='average_degree':
        metric = np.mean([d for n, d in graph.degree() if d!=0])
    elif METRIC=='average_local_efficiency':
        metric = nx.local_efficiency(graph)
    elif METRIC=='global_efficiency':
        metric = nx.global_efficiency(graph)
    elif METRIC=='local_efficiency':
        metric = [nx.global_efficiency(graph.subgraph(graph[v])) for v in graph]
    elif METRIC=='betweeness_centrality':
        metric = np.asarray(list(nx.betweenness_centrality(graph).values()))
    elif METRIC=='eigenvector_centrality':
        metric = np.asarray(list(nx.eigenvector_centrality(graph).values()))
    elif METRIC=='degree_centrality':
        metric = np.asarray(list(nx.degree_centrality(graph).values()))
    elif METRIC=='modularity':
        metric = modularity_louvain(graph)
    elif METRIC=='modularity_macroareas':
        metric = modularity_macroareas(graph, macro_areas_list)
        
    return metric

def cort_subcort_connectivity(adj, full_c_sc_link, subcortical_idxs, cortical_idxs):
    # Take only the cortico-subcortical link
    sub_meanchia = adj[subcortical_idxs]
    sub_meanchia[:,subcortical_idxs]=0
    # number of cortico-subcortical link
    perc_c_sc_link = np.sum(sub_meanchia)/full_c_sc_link
    
    return perc_c_sc_link
    
def homotopic_connectivity(adj, full_c_sc_link):
    # Inter hemispheric connections
    
    cort_homo = np.sum(adj[[x for x in range(0,100)], [x for x in range(100,200)]])
    
    subcort_mat = np.copy(adj[200:232,200:232])
    subcort_homo = np.sum(subcort_mat[[x for x in range(0,16)], [x for x in range(16,32)]])
    
    scoll_homo = np.sum(adj[-1,-2])
    
    homo_conn = cort_homo + scoll_homo + subcort_homo
    
    return homo_conn
    

# Metrics on directed graph
def directed_global_efficiency(G):
    n = len(G)
    sum_efficiency = 0
    paths = dict(nx.all_pairs_dijkstra_path_length(G))
    for i in G.nodes():
        for j in G.nodes():
            if i != j:
                try:
                    sum_efficiency += 1 / paths[i][j]
                except KeyError:
                    continue  # no path from i to j, skip this pair
    if n > 1:
        global_efficiency = sum_efficiency / (n * (n - 1))
    else:
        global_efficiency = 0  # handle case with one or no nodes
    return global_efficiency
    
def average_shortest_path_length_directed(G):
    if nx.is_strongly_connected(G):
        # Use the built-in function if the graph is strongly connected
        return nx.average_shortest_path_length(G)
    else:
        # Calculate the average only over reachable pairs
        path_lengths = []
        for i in G.nodes():
            lengths = nx.single_source_dijkstra_path_length(G, i)
            path_lengths.extend(lengths.values())
        
        if path_lengths:
            return sum(path_lengths) / len(path_lengths)
        else:
            return float('inf')  # or some other appropriate value

def DiModularity(adj):
    g = ig.Graph.Adjacency(adj, mode='directed')
    # The method `community_infomap` is one example that can handle directed graphs
    communities = g.community_infomap()
    # Extract the membership vector for coloring
    membership = communities.membership
    # Calculate modularity
    modularity_score = communities.modularity
    return modularity_score

def DiModularity_macroareas(adj, mas_list_node):
    g = ig.Graph.Adjacency(adj, mode='directed')
    membership = mas_list_node
    # Calculate modularity
    modularity_score = g.modularity(membership, directed=True)
    return modularity_score

def Digraph_metrics(METRIC, graph, adj, mas_list_node):
    if METRIC=='global_efficiency':
        metric = directed_global_efficiency(graph)
    elif METRIC=='average_shortest_path':
        metric = average_shortest_path_length_directed(graph)
    elif METRIC=='modularity':
        metric = DiModularity(adj)
    elif METRIC=='modularity_macroareas':
        metric = DiModularity_macroareas(adj, mas_list_node)
        
    return metric