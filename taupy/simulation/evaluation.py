from igraph import Graph, ADJ_MAX
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering
from concurrent.futures import ProcessPoolExecutor
from taupy import (difference_matrix, group_divergence, group_consensus, group_size_parity,
                   normalised_hamming_distance, pairwise_dispersion, number_of_groups)
import numpy as np
import pandas as pd

def evaluate_experiment(experiment, *, function=None, densities=True, executor={}):
    with ProcessPoolExecutor(**executor) as executor:
        results = [executor.submit(function, simulation=i) for i in experiment]
    
    return pd.concat([i.result() for i in results], keys=[n for n, _ in enumerate(results)])

def variance_dispersion(simulation, *, densities=True):
    if densities:
        densities = [i.density() for i in simulation]

    dispersions = [pairwise_dispersion(i, measure=normalised_hamming_distance) for i in simulation.positions]
    
    if dispersions:
        return pd.DataFrame(list(zip(densities, dispersions)), columns=["density", "dispersion"])
    else:
        return dispersions

def group_measures_leiden(simulation, *, densities=True):
    if densities:
        densities = [i.density() for i in simulation]

    matrices = [difference_matrix(i, measure=normalised_hamming_distance) for i in simulation.positions]
    filtered_matrices = [np.exp(-4 * i.astype("float64")) for i in matrices]
    
    for i in filtered_matrices:
        np.fill_diagonal(i, 0)
        # Assume number of positions is homogenous.
        i[np.triu_indices(len(simulation.positions[0]))] = 0
        i[i<0.2] = 0
    
    graphs = [Graph.Weighted_Adjacency(i.astype("float64").tolist(), mode=ADJ_MAX) for i in filtered_matrices]
    clusterings = [list(g.community_leiden(weights="weight", objective_function="modularity")) for g in graphs]
    divergences = [group_divergence(i, matrices[num]) for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, numbers, size_parity)), 
                            columns=["density", "divergence", "consensus", "numbers", "size_parity"])
    else:
        return divergences

def group_measures_agglomerative(simulation, *, densities=True):
    if densities:
        densities = [i.density() for i in simulation]

    matrices = [difference_matrix(i, measure=normalised_hamming_distance) for i in simulation.positions]
    agglomerative = [AgglomerativeClustering(affinity="precomputed", 
                                             n_clusters=None, 
                                             compute_full_tree=True, 
                                             distance_threshold=.75, 
                                             linkage="complete").fit(i) for i in matrices]
    
    clusters = [[[i[0] for i in enumerate(k.labels_) if i[1] == j] for j in range(k.n_clusters_)] for k in agglomerative]
    divergences = [group_divergence(i, matrices[num]) for num, i in enumerate(clusters)]
    consensus = [group_consensus(i, matrices[num]) for num, i in enumerate(clusters)]
    numbers = [number_of_groups(i) for i in clusters]
    size_parity = [group_size_parity(i) for i in clusters]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, numbers, size_parity)), 
                            columns=["density", "divergence", "consensus", "numbers", "size_parity"])
    else:
        return divergences


def group_measures_affinity_propagation(simulation, *, densities=True):
    if densities:
        densities = [i.density() for i in simulation]
    
    matrices = [difference_matrix(i, measure=normalised_hamming_distance) for i in simulation.positions]
    filtered_matrices = [np.exp(-4 * i.astype("float64")) for i in matrices]
    
    for i in filtered_matrices:
        np.fill_diagonal(i, 0)
        # Assume number of positions is homogenous.
        i[np.triu_indices(len(simulation.positions[0]))] = 0
        i[i<0.2] = 0

    fits = [AffinityPropagation(affinity="precomputed", random_state=0).fit(i) for i in filtered_matrices]
    clusterings = [[[i[0] for i in enumerate(k.labels_) if i[1] == j] for j in range(len(k.cluster_centers_indices_))] for k in fits]
    divergences = [group_divergence(i, matrices[num]) for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    #size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, numbers)), 
                            columns=["density", "divergence", "consensus", "numbers"])
    else:
        return divergences
