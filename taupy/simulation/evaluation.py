from igraph import Graph, ADJ_MAX
from taupy import difference_matrix, group_divergence, normalised_hamming_distance
import numpy as np

def evaluate_experiment_with_leiden(experiment, *, densities=True):

    if densities:
        densities = [[i.density() for i in j] for j in experiment]

    matrices = [[difference_matrix(i, measure=normalised_hamming_distance) for i in j.positions] for j in experiment]
    filtered_matrices = [[np.exp(-4 * i.astype("float64")) for i in m] for m in matrices]
    
    for j in filtered_matrices:
        for i in j:
            np.fill_diagonal(i, 0)
            # Assume number of positions is homogenous in the complete
            # experiment.
            i[np.triu_indices(len(experiment[0].positions[0]))] = 0
            i[i<0.2] = 0
    
    graphs = [[Graph.Weighted_Adjacency(i.astype("float64").tolist(), mode=ADJ_MAX) for i in j] for j in filtered_matrices]
    clusterings = [[list(i.community_leiden(weights="weight", objective_function="modularity")) for i in g] for g in graphs]
    divergences = [[group_divergence(i, matrices[mnum][num]) for num, i in enumerate(j)] for mnum, j in enumerate(clusterings)]

    if densities:
        return (densities, divergences)
    else:
        return divergences