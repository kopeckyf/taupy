from igraph import Graph, ADJ_MAX
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering
from concurrent.futures import ProcessPoolExecutor
from taupy import (difference_matrix, group_divergence, group_consensus, group_size_parity,
                   normalised_hamming_distance, hamming_distance, edit_distance, 
                   normalised_edit_distance, pairwise_dispersion, number_of_groups, 
                   bna, satisfiability_count)
from statistics import mean
import numpy as np
import pandas as pd

def evaluate_experiment(experiment, *, function=None, densities=True, executor={}, arguments={}):
    with ProcessPoolExecutor(**executor) as executor:
        results = [executor.submit(function, simulation=i, **arguments) for i in experiment]
    
    return pd.concat([i.result() for i in results], keys=[n for n, _ in enumerate(results)])

def position_changes(simulation, *, measure=hamming_distance, densities=True):
    if densities:
        densities = [i.density() for i in simulation]
    
    #pairs of debate stages
    p = [simulation.positions[i:i+2] for i in range(len(simulation.positions)-1)]
    averages = []
    
    for pair in p:
        d = [measure(pair[0][i], pair[1][i]) for i in range(len(pair[0]))]
        averages.append(len([pos for pos in d if pos != 0]))
    
    density_pairs = [mean(densities[i:i+2]) for i in range(len(densities)-1)]
    
    if densities:
        return pd.DataFrame(list(zip(density_pairs, averages)), columns=["avg density in pair", "position difference"])
    else:
        return averages
    

def mean_population_wide_agreement(simulation, *, densities=True):
    if densities:
        densities = [i.density() for i in simulation]
    
    matrices = [difference_matrix(i, measure=bna) for i in simulation.positions]
    agreement = [i[np.triu_indices(len(simulation.positions[0]), k=1)].mean() for i in matrices]
    
    if densities:
        return pd.DataFrame(list(zip(densities, agreement)), columns=["density", "agreement"])
    else:
        return agreement

def auxiliary_information(simulation):
    size_of_sccp = [satisfiability_count(i) for i in simulation]
    unique_positions = [len([dict(i) for i in set(frozenset(position.items()) for position in stage)]) for stage in simulation.positions]

    return pd.DataFrame(list(zip(size_of_sccp, unique_positions)), columns=["sccp_extension", "number_uniq_pos"])

def variance_dispersion(simulation, *, measure=normalised_hamming_distance, densities=True):
    if densities:
        densities = [i.density() for i in simulation]

    dispersions = [pairwise_dispersion(i, measure=measure) for i in simulation.positions]
    
    if densities:
        return pd.DataFrame(list(zip(densities, dispersions)), columns=["density", "dispersion"])
    else:
        return dispersions

def variance_dispersion_partial_positions(simulation, *, measure=normalised_edit_distance, densities=True):
    if densities:
        densities = [i.density() for i in simulation]

    dispersions = [pairwise_dispersion(i, measure=measure) for i in simulation.positions]
    
    if densities:
        return pd.DataFrame(list(zip(densities, dispersions)), columns=["density", "dispersion"])
    else:
        return dispersions
    
def group_measures_exogenous(simulation, *, sentence=None, densities=True):
    if densities:
        densities = [i.density() for i in simulation]

    matrices = [difference_matrix(i, measure=edit_distance)/len(set.union(*[set(j) for j in i])) for i in simulation.positions]
    
    clusterings = []
    for i in simulation.positions:
        accepting_positions = []
        rejecting_positions = []
        suspending_positions = []
        for num, pos in enumerate(i):
            if sentence in pos:
                if pos[sentence] == True:
                    accepting_positions.append(num)
                if pos[sentence] == False:
                    rejecting_positions.append(num)
            else:
                suspending_positions.append(num)
        clusterings.append([accepting_positions, rejecting_positions, 
                            suspending_positions])  
    
    divergences = [group_divergence(i, matrices[num]) for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, numbers, size_parity)), 
                            columns=["density", "divergence", "consensus", "numbers", "size_parity"])
    else:
        return divergences

def group_measures_leiden(simulation, *, densities=True, key_propositions=None):
    if densities:
        densities = [i.density() for i in simulation]

    matrices = [difference_matrix(i, measure=normalised_hamming_distance) for i in simulation.positions]
    
    if key_propositions == None:
        clustering_matrices = matrices
    else:
        filtered_positions = [[{k: j[k] for k in key_propositions} for j in i] for i in simulation.positions]
        clustering_matrices = [difference_matrix(i, measure=normalised_hamming_distance) for i in filtered_positions]
        
    filtered_matrices = [np.exp(-4 * i.astype("float64")) for i in clustering_matrices]
    
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

def group_measures_leiden_partial_positions(simulation, *, densities=True, key_propositions=None):
    if densities:
        densities = [i.density() for i in simulation]

    matrices = [difference_matrix(i, measure=edit_distance)/len(set.union(*[set(j) for j in i])) for i in simulation.positions]

    if key_propositions == None:
        clustering_matrices = matrices
    else:
        filtered_positions = [[{k: j[k] for k in key_propositions if k in j} for j in i] for i in simulation.positions]
        clustering_matrices = [difference_matrix(i, measure=edit_distance)/len(set.union(*[set(j) for j in i])) for i in filtered_positions]

    filtered_matrices = [np.exp(-4 * i.astype("float64")) for i in clustering_matrices]
    
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

def group_measures_affinity_propagation_partial_positions(simulation, *, densities=True):
    if densities:
        densities = [i.density() for i in simulation]
    
    matrices = [difference_matrix(i, measure=edit_distance)/len(set.union(*[set(j) for j in i])) for i in simulation.positions]
    filtered_matrices = [np.exp(-4 * i.astype("float64")) for i in matrices]

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
