"""
Clusterings are required by other analysis modules, such as diversity and 
polarisation functions.
"""
import numpy as np
from igraph import Graph, ADJ_MAX
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering, DBSCAN

from taupy.analysis.polarisation import difference_matrix
from taupy.analysis.agreement import normalised_hamming_distance

def clustering_matrices(positions, *, measure=normalised_hamming_distance, 
                        scale=-4, distance_threshold=0.2):
    """
    Converts difference matrices to sparse clustering matrices that can be input
    to community structuring algorithms. This is necessary because many 
    clustering algorithms are designed for sparse social networks.
    """

    diff_matrices = [difference_matrix(i, measure=measure) for i in positions]

    if scale is not None:
        filtered_matrices = [np.exp(scale * i.astype("float64")) 
                             for i in diff_matrices]  
    else:
        filtered_matrices = diff_matrices

    for i in filtered_matrices:
        # Create a triangle filtered triangle matrix
        np.fill_diagonal(i, 0)
        i[np.triu_indices(len(positions[0]))] = 0
        # All cells below the filter threshold are flattened.
        i[i < distance_threshold] = 0

    return filtered_matrices

def leiden(clustering_matrices):
    """
    Return the community structure obtained by the Leiden clustering algorithm.
    ------
    References:
    Traag, V. A., Waltman, L. & van Eck, N. J. (2019). From Louvain to Leiden: 
    Guaranteeing well-connected communities. Scientific Reports, 9. 
    DOI: 10/gfxg2v
    """
    # Creates igraph Graph objects from clustering matrices.
    graphs = [Graph.Weighted_Adjacency(
                i.astype("float64").tolist(), mode=ADJ_MAX) \
                    for i in clustering_matrices]
    # Perform the community_leiden() method on the Graph objects and return
    return [list(g.community_leiden(
                    weights="weight", objective_function="modularity")) \
                        for g in graphs]

def affinity(clustering_matrices):
    """
    Return the community structure obtained by clustering with Affinity 
    Propagation.
    -------
    References:
    Frey, B. J. & Dueck, D. (2007). Clustering by passing messages between data
    points. Science, 315(5814), 972–976. DOI: 10.1126/science.1136800.
    """
    fits = [AffinityPropagation(affinity="precomputed", random_state=0).fit(i) 
            for i in clustering_matrices]
    return [[[i[0] for i in enumerate(k.labels_) if i[1] == j] 
             for j in range(len(k.cluster_centers_indices_))] 
             for k in fits]

def agglomerative(clustering_matrices, *, distance_threshold=0.75):
    """
    Return community structuring obtained by Agglomerative Clustering. 
    """
    agglomerative = [AgglomerativeClustering(
                        affinity="precomputed", 
                        n_clusters=None, 
                        compute_full_tree=True, 
                        distance_threshold=distance_threshold, 
                        linkage="complete").fit(i) for i in clustering_matrices]
    
    return [[[i[0] for i in enumerate(k.labels_) if i[1] == j] 
                for j in range(k.n_clusters_)]
                for k in agglomerative]

def density_based_clustering(matrices, *, min_cluster_size=3, 
                             max_neighbour_distance=0.2):
    """
    Return community structure obtained from density based clustering. This
    clustering algorithm allows noise. Points with -1 signal noise.
    """
    return [DBSCAN(eps=max_neighbour_distance, min_samples=min_cluster_size,
                   metric="precomputed").fit(i).labels_ for i in matrices]