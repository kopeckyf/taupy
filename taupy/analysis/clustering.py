"""
Clusterings are required by other analysis modules, such as diversity and 
polarisation functions.
"""
import numpy as np
from igraph import Graph
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering, DBSCAN

from taupy.analysis.agreement import (normalised_hamming_distance, 
                                      difference_matrix)

def clustering_matrix(positions, *, measure=normalised_hamming_distance, 
                      scale=-4, distance_threshold=0.2):
    """
    Converts a difference matrix to a sparse clustering (adjacency) matrix that 
    can be input to the Leiden and affinity propagation community structuring 
    algorithms. These clustering algorithms are designed for sparse adjacency
    matrices.

    Other clustering algorithms, like agglomerative clustering, work on 
    difference matrices. This function should not be used with these algorithms.

    The default scale of -4 and threshold of 0.2 implies that agent pairs with a 
    normalised δ > 0.4 will be considered with 0 adjacency in clustering. With a 
    scale of -2, only agent paris with normalised δ > 0.8 are filtered.
    """

    diff_matrix = difference_matrix(positions, measure=measure)

    if scale is not None:
        filtered_matrix = np.exp(scale * diff_matrix.astype("float64"))
    else:
        filtered_matrix = diff_matrix

    # All cells below the filter threshold are flattened.
    filtered_matrix[filtered_matrix < distance_threshold] = 0

    return filtered_matrix

def leiden(positions, *, clustering_settings={}, 
           algorithm_settings={
               "weights": "weight", "objective_function": "modularity"
               }
          ):
    """
    Return the community structure obtained by the Leiden clustering algorithm
    (see [Traag2019]_).
    """
    matrix = clustering_matrix(positions=positions, **clustering_settings)

    # Creates igraph Graph objects from clustering matrices.
    graph = Graph.Weighted_Adjacency(
                matrix.astype("float64").tolist(), mode="max"
            )
    # Perform the community_leiden() method on the Graph objects and return
    return list(graph.community_leiden(**algorithm_settings))

def affinity_propagation(positions, *, clustering_settings={},
                         algorithm_settings={
                             "affinity": "precomputed", 
                             "random_state": 0,
                             "max_iter": 1000
                         }):
    """
    Return the community structure obtained by clustering with Affinity 
    Propagation ([Frey2007]_).
    """
    matrix = clustering_matrix(positions=positions, **clustering_settings)
    fits = AffinityPropagation(**algorithm_settings).fit(matrix) 
    return [[i[0] for i in enumerate(fits.labels_) if i[1] == j] 
             for j in range(len(fits.cluster_centers_indices_))
           ] 

def agglomerative_clustering(positions, *, distance_threshold=0.75,
                             base_measure=normalised_hamming_distance):
    """
    Return community structuring obtained by Agglomerative Clustering. Please
    note that Agglomerative Clustering accepts a common difference matrix, *not* 
    an adjacency matrix as Leiden and Affinity Propagation do. It is not
    advisable to pass the output of clustering_matrix() to this function. 
    Please use difference_matrix() with a normalised distance measure as input.
    """
    matrix = difference_matrix(positions=positions, measure=base_measure)

    agglomerative = AgglomerativeClustering(
                        affinity="precomputed", 
                        n_clusters=None, 
                        compute_full_tree=True, 
                        distance_threshold=distance_threshold, 
                        linkage="complete"
                    ).fit(matrix)
    
    return [[i[0] for i in enumerate(agglomerative.labels_) if i[1] == j] 
                for j in range(agglomerative.n_clusters_)
           ]

def density_based_clustering(positions, *, min_cluster_size=3, 
                             max_neighbour_distance=0.2, 
                             base_measure=normalised_hamming_distance):
    """
    Return community structure obtained from density based clustering on
    a distance (not adjacency) matrix. This clustering algorithm is the only
    one implemented in this module to allow noise. Points with -1 signal noise.
    """
    matrix = difference_matrix(positions=positions, measure=base_measure)

    return DBSCAN(
                eps=max_neighbour_distance, 
                min_samples=min_cluster_size,
                metric="precomputed").fit(matrix).labels_ 

def clustering_based_on_stance(positions, *, proposition, 
                               truth_values=[True, False, None]):
    """
    An exogenous clustering method based on the positions' stances toward a 
    selected proposition. Cluster number is always equal to number of truth
    values, but may contain empty clusters. 
    """

    dict_of_tva = {t: [] for t in truth_values}

    for i, p in enumerate(positions):
        if proposition in p:
            dict_of_tva[p[proposition]].append(i)
    
    return [dict_of_tva[key] for key in dict_of_tva]            