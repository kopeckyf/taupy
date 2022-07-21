from igraph import Graph, ADJ_MAX
from sklearn.cluster import AffinityPropagation, AgglomerativeClustering
from concurrent.futures import ProcessPoolExecutor
from taupy import (difference_matrix, group_divergence, group_consensus, 
                   group_size_parity, normalised_hamming_distance, 
                   hamming_distance, edit_distance, normalised_edit_distance, 
                   pairwise_dispersion, number_of_groups, bna, satisfiability, 
                   satisfiability_count, Position, Debate, EmptyDebate)
from statistics import mean
from collections import Counter
import numpy as np
import pandas as pd
from random import choices

def evaluate_experiment(experiment,
                        *, 
                        function, 
                        data_type="pickle", 
                        executor={}, 
                        arguments={"densities": True, 
                                   "progress": False}
                        ):
    """
    A function that applies an evaluation `function` to a collection of 
    Simulations from an `experiment`. Simulations return different data formats,
    hence the option to specify a `data_type`. `arguments` are passed to the 
    evaluation function and need to be chosen based on the required arguments
    of the functions. Every `function` in this module is designed to be applied
    with `evaluate_experiment()`.
    """

    if data_type not in ["pickle", "FixedDebate", "SocialInfluence"]:
        raise NotImplementedError(
            f"There is no recipe for data type {data_type}."
        )

    with ProcessPoolExecutor(**executor) as executor:
        if data_type == "pickle":
            results = [executor.submit(function, 
                                       debate_stages=i, 
                                       positions=i.positions,
                                       **arguments) for i in experiment]
        if data_type == "FixedDebate":
            results = [executor.submit(function, 
                                       debate_stages=[EmptyDebate(), 
                                                      *[Debate(*i["uncovered_arguments"][:j])
                                                        for j in range(
                                                            1, len(i["uncovered_arguments"])+1)
                                                        ]],
                                       positions=i["positions"], 
                                       **arguments) for i in experiment]
        
        if data_type == "SocialInfluence":
            results = [executor.submit(function,
                                       debate_stages=[i["debate"] \
                                         for _ in range(len(i["positions"]))],
                                       positions=i["positions"],
                                       **arguments) for i in experiment]

    return pd.concat([i.result() for i in results], 
                     keys=[n for n, _ in enumerate(results)])

def majority_voting(debate_stages, 
                    *, 
                    positions,
                    sentencepool,
                    key_statements=None,
                    densities=True,
                    progress=False,
                    method="all",
                    measure_agreement=bna):
    """
    Voting algorithm
    """
    if densities:
        densities = [i.density() for i in debate_stages]

    if progress:
        progress = [(i+1)/len(debate_stages) for i in range(len(debate_stages))]

    majority_closed = []
    majority_coherent = []
    agreement = []

    for stage, plist in enumerate(positions):
        if method == "all":
            vote_none = Counter([x for l in [[s for s in sentencepool if s not in i] for i in plist] for x in l])
            vote_true = Counter([x for l in [[s for s in i if i[s]==True] for i in plist] for x in l])
            vote_false = Counter([x for l in [[s for s in i if i[s]==False] for i in plist] for x in l])

        if method == "key":
            if key_statements is None:
                raise ValueError("No key statements supplied.")
            vote_none = Counter([x for l in [[s for s in key_statements if s not in i] for i in plist] for x in l])
            vote_true = Counter([x for l in [[s for s in key_statements if s in i and i[s]==True] for i in plist] for x in l])
            vote_false = Counter([x for l in [[s for s in key_statements if s in i and  i[s]==False] for i in plist] for x in l])

        v = pd.merge(pd.DataFrame.from_dict(vote_none, orient="index", columns=["None"]),
                     pd.merge(pd.DataFrame.from_dict(vote_true, orient="index", columns=["True"]),
                              pd.DataFrame.from_dict(vote_false, orient="index", columns=["False"]), 
                              how="outer", 
                              left_index=True, 
                              right_index=True), 
                     how="outer", 
                     left_index=True, 
                     right_index=True).fillna(0)
        
        d = v.apply("idxmax",axis=1).to_dict()
        pos = Position(debate_stages[stage], 
                       {k: True for k in d if d[k] == "True"} \
                       | {k: False for k in d if d[k] == "False"})
        
        majority_closed.append(pos.is_closed())
        majority_coherent.append(pos.is_coherent())

        if measure_agreement is not None:
            m = difference_matrix(plist, measure=measure_agreement)
            agreement.append(m[np.triu_indices(len(positions[0]), k=1)].mean())
        else:
            agreement.append("not calculated")

    if densities or progress:

        if not progress:
            return pd.DataFrame(list(zip(densities, majority_closed, 
                                         majority_coherent, agreement)),
                                columns=["density", "majority is closed", 
                                         "majority is coherent", "agreement"])

        if not densities:
            return pd.DataFrame(list(zip(progress, majority_closed, 
                                         majority_coherent, agreement)),
                                columns=["progress", "majority is closed", 
                                         "majority is coherent", "agreement"])

        if progress and densities:
            return pd.DataFrame(list(zip(progress, densities, majority_closed, 
                                         majority_coherent, agreement)),
                                columns=["progress", "density", 
                                         "majority is closed", 
                                         "majority is coherent",
                                         "agreement"])

    else:
        return pd.DataFrame(list(zip(majority_closed, majority_coherent, 
                                     agreement)))


def majority_voting_among_random_sample(debate_stages,
                                        *, 
                                        n_positions,
                                        sentencepool,
                                        key_statements=None,
                                        densities=True,
                                        progress=False,
                                        method="all",
                                        measure_agreement=bna):

    """
    Before majority voting, pick `n_positions` number of coherent positions
    for the respective debate stage. Then return the voting result among these
    positions. It is important to pick random positions with replacement in case
    there are fewer coherent positions relative to the debate stage then asked 
    for in `n_positions`.
    """

    random_positions = []

    for i in debate_stages:
        sat = satisfiability(i, all_models=True)
        # Pick positions with replacement
        random_positions.append(choices(sat, k=n_positions))

    return majority_voting(debate_stages=debate_stages,
                           positions=random_positions,
                           sentencepool=sentencepool,
                           key_statements=key_statements,
                           densities=densities,
                           progress=progress,
                           method=method,
                           measure_agreement=measure_agreement)


def position_changes(debate_stages, 
                     *, 
                     positions,
                     measure=hamming_distance, 
                     densities=True,
                     progress=False):
    
    #pairs of debate stages
    p = [positions[i:i+2] for i in range(len(positions)-1)]
    averages = []
    
    for pair in p:
        d = [measure(pair[0][i], pair[1][i]) for i in range(len(pair[0]))]
        averages.append(len([pos for pos in d if pos != 0]))

    if densities:
        densities = [i.density() for i in debate_stages]
        density_pairs = [mean(densities[i:i+2]) for i in range(len(densities)-1)]

    if progress:
        progress = [(i+1) / len(debate_stages) for i in range(len(debate_stages))]
        progress_pairs = [mean(progress[i:i+2]) for i in range(len(progress)-1)]
    
    if densities or progress:
        if not progress:
            return pd.DataFrame(list(zip(density_pairs, averages)), 
                                columns=["avg density in pair", 
                                         "position difference"])
        
        if not densities:
            return pd.DataFrame(list(zip(progress_pairs, averages)), 
                                columns=["avg progress in pair", 
                                         "position difference"])

        if densities and progress:
            return pd.DataFrame(list(zip(density_pairs, progress_pairs, averages)), 
                                columns=["avg density in pair", 
                                         "avg progress in pair",
                                         "position difference"])

    else:
        return averages

def len_of_positions(debate_stages, 
                     *, 
                     positions):
    sim_ids = [idx for idx, _ in enumerate(debate_stages)]

    int1 = len([p for p in positions[-1] if len(p) in list(range(0,7))])
    int2 = len([p for p in positions[-1] if len(p) in list(range(7,14))])
    int3 = len([p for p in positions[-1] if len(p) in list(range(14,21))])

    return pd.DataFrame(list(zip(sim_ids, int1, int2, int3)), 
                        columns=["id", "0–6", "7–13", "14–20"])
    

def mean_population_wide_agreement(*,
                                   debate_stages,
                                   positions,
                                   densities=True, 
                                   progress=False, 
                                   measure=bna):

    if densities:
        densities = [i.density() for i in debate_stages]

    if progress:
        progress = [(i+1)/len(debate_stages) for i in range(len(debate_stages))]
    
    matrices = [difference_matrix(i, measure=measure) for i in positions]
    agreement = [i[np.triu_indices(len(positions[0]), k=1)].mean() for i in matrices]
    
    if densities and not progress:
        return pd.DataFrame(list(zip(densities, agreement)), 
                            columns=["density", "agreement"])
    
    if progress and not densities:
        return pd.DataFrame(list(zip(progress, agreement)), 
                            columns=["progress", "agreement"])

    if densities and progress:
        return pd.DataFrame(list(zip(densities, progress, agreement)), 
                            columns=["densities", "progress", "agreement"])

    if not (densities or progress):
        return pd.Series(agreement)

def auxiliary_information(debate_stages, *, positions):
    size_of_sccp = [satisfiability_count(i) for i in debate_stages]
    unique_positions = [len([dict(i) for i in set(frozenset(position.items())
                             for position in stage)])
                        for stage in positions]

    return pd.DataFrame(list(zip(size_of_sccp, unique_positions)), 
                        columns=["sccp_extension", "number_uniq_pos"])

def variance_dispersion(*,
                        debate_stages,
                        positions,
                        measure=normalised_hamming_distance, 
                        densities=True,
                        progress=False):
    if densities:
        densities = [i.density() for i in debate_stages]

    if progress:
        progress = [(i+1)/len(debate_stages) for i in range(len(debate_stages))]

    dispersions = [pairwise_dispersion(i, measure=measure) for i in positions]
    
    if densities or progress:
        if not progress:
            df = list(zip(densities, dispersions))
            col = ["density", "dispersion"]

        if not densities: 
            df = list(zip(progress, dispersions))
            col = ["progress", "dispersion"]

        if densities and progress:
            df = list(zip(densities, progress, dispersions))
            col = ["densities", "progress", "dispersion"]

        return pd.DataFrame(df, columns=col)
    else:
        return dispersions
    
def group_measures_exogenous(debate_stages, 
                             *, 
                             positions,
                             sentence=None, 
                             densities=True):
    if densities:
        densities = [i.density() for i in debate_stages]

    matrices = [difference_matrix(i, measure=edit_distance)
                / len(set.union(*[set(j) for j in i])) for i in positions]
    
    clusterings = []
    for i in positions:
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
    
    divergences = [group_divergence(i, matrices[num]) 
                   for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) 
                 for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, 
                                     numbers, size_parity)), 
                            columns=["density", "divergence", "consensus", 
                                     "numbers", "size_parity"])
    else:
        return pd.Series(divergences)

def group_measures_leiden(debate_stages, 
                          *,
                          positions,
                          densities=True, 
                          progress=False,
                          key_propositions=None):

    if densities:
        densities = [i.density() for i in debate_stages]

    matrices = [difference_matrix(i, measure=normalised_hamming_distance) for i in positions]
    
    if key_propositions == None:
        clustering_matrices = matrices
    else:
        filtered_positions = [[{k: j[k] for k in key_propositions} for j in i] 
                              for i in positions]
        clustering_matrices = [difference_matrix(i, measure=normalised_hamming_distance) \
                               for i in filtered_positions]
        
    filtered_matrices = [np.exp(-4 * i.astype("float64")) 
                         for i in clustering_matrices]
    
    for i in filtered_matrices:
        np.fill_diagonal(i, 0)
        # Assume number of positions is homogenous.
        i[np.triu_indices(len(positions[0]))] = 0
        i[i<0.2] = 0
    
    graphs = [Graph.Weighted_Adjacency(i.astype("float64").tolist(), 
                                       mode=ADJ_MAX) 
              for i in filtered_matrices]
    clusterings = [list(g.community_leiden(weights="weight", 
                                           objective_function="modularity")) 
                   for g in graphs]
    divergences = [group_divergence(i, matrices[num]) 
                   for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) 
                 for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, numbers, size_parity)), 
                            columns=["density", "divergence", "consensus", "numbers", "size_parity"])
    else:
        return pd.Series(divergences)

def group_measures_agglomerative(debate_stages, 
                                 *,
                                 positions,
                                 densities=True,
                                 progress=False):
    if densities:
        densities = [i.density() for i in debate_stages]

    matrices = [difference_matrix(i, measure=normalised_hamming_distance) 
                for i in positions]
    agglomerative = [AgglomerativeClustering(affinity="precomputed", 
                                             n_clusters=None, 
                                             compute_full_tree=True, 
                                             distance_threshold=.75, 
                                             linkage="complete").fit(i) 
                     for i in matrices]
    
    clusters = [[[i[0] for i in enumerate(k.labels_) if i[1] == j] 
                 for j in range(k.n_clusters_)]
                for k in agglomerative]
    divergences = [group_divergence(i, matrices[num]) 
                   for num, i in enumerate(clusters)]
    consensus = [group_consensus(i, matrices[num]) 
                 for num, i in enumerate(clusters)]
    numbers = [number_of_groups(i) for i in clusters]
    size_parity = [group_size_parity(i) for i in clusters]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, 
                                     numbers, size_parity)), 
                            columns=["density", "divergence", "consensus", 
                                     "numbers", "size_parity"])
    else:
        return pd.Series(divergences)

def group_measures_leiden_partial_positions(debate_stages, 
                                            *,
                                            positions,
                                            densities=True, 
                                            progress=False, 
                                            key_propositions=None):
    if densities:
        densities = [i.density() for i in debate_stages]

    matrices = [difference_matrix(i, measure=edit_distance)
                / len(set.union(*[set(j) for j in i])) for i in positions]

    if key_propositions == None:
        clustering_matrices = matrices
    else:
        filtered_positions = [[{k: j[k] for k in key_propositions if k in j} 
                               for j in i] for i in positions]
        clustering_matrices = [difference_matrix(i, measure=edit_distance)
                               / len(set.union(*[set(j) for j in i])) 
                               for i in filtered_positions]

    filtered_matrices = [np.exp(-4 * i.astype("float64")) 
                         for i in clustering_matrices]
    
    graphs = [Graph.Weighted_Adjacency(i.astype("float64").tolist(), 
                                       mode=ADJ_MAX) 
              for i in filtered_matrices]
    clusterings = [list(g.community_leiden(weights="weight", 
                                           objective_function="modularity")) 
                   for g in graphs]
    divergences = [group_divergence(i, matrices[num]) 
                   for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) 
                 for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, 
                                     numbers, size_parity)), 
                            columns=["density", "divergence", "consensus", 
                                     "numbers", "size_parity"])
    else:
        return pd.Series(divergences)


def group_measures_affinity_propagation(debate_stages, 
                                        *, 
                                        positions,
                                        densities=True,
                                        progress=False):
    if densities:
        densities = [i.density() for i in debate_stages]
    
    matrices = [difference_matrix(i, measure=normalised_hamming_distance) 
                for i in positions]
    filtered_matrices = [np.exp(-4 * i.astype("float64")) for i in matrices]
    
    for i in filtered_matrices:
        np.fill_diagonal(i, 0)
        # Assume number of positions is homogenous.
        i[np.triu_indices(len(positions[0]))] = 0
        i[i<0.2] = 0

    fits = [AffinityPropagation(affinity="precomputed", random_state=0).fit(i) 
            for i in filtered_matrices]
    clusterings = [[[i[0] for i in enumerate(k.labels_) if i[1] == j] 
                    for j in range(len(k.cluster_centers_indices_))] 
                   for k in fits]
    divergences = [group_divergence(i, matrices[num]) 
                   for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) 
                 for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    #size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, 
                                     numbers)), 
                            columns=["density", "divergence", "consensus", 
                                     "numbers"])
    else:
        return pd.Series(divergences)

def group_measures_affinity_propagation_partial_positions(debate_stages, 
                                                          *,
                                                          positions,
                                                          densities=True,
                                                          progress=False):
    if densities:
        densities = [i.density() for i in debate_stages]
    
    matrices = [difference_matrix(i, measure=edit_distance)
                / len(set.union(*[set(j) for j in i])) for i in positions]
    filtered_matrices = [np.exp(-4 * i.astype("float64")) for i in matrices]

    fits = [AffinityPropagation(affinity="precomputed", random_state=0).fit(i) 
            for i in filtered_matrices]
    clusterings = [[[i[0] for i in enumerate(k.labels_) if i[1] == j] 
                    for j in range(len(k.cluster_centers_indices_))] 
                   for k in fits]
    divergences = [group_divergence(i, matrices[num]) 
                   for num, i in enumerate(clusterings)]
    consensus = [group_consensus(i, matrices[num]) 
                 for num, i in enumerate(clusterings)]
    numbers = [number_of_groups(i) for i in clusterings]
    #size_parity = [group_size_parity(i) for i in clusterings]

    if densities:
        return pd.DataFrame(list(zip(densities, divergences, consensus, 
                                     numbers)), 
                            columns=["density", "divergence", "consensus", 
                                     "numbers"])
    else:
        return pd.Series(divergences)
