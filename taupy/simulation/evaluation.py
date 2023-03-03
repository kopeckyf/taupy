"""
Functions for evaluating multiple data points, such as Simulations or Experiments.
Compared to the functions in the :py:mod:`analysis` modules, the functions in 
this module operate on collections of objects. The analysis functions provide 
the atomic measures for these operations.
"""

from concurrent.futures import ProcessPoolExecutor
from taupy import (difference_matrix, group_divergence, group_consensus, 
                   normalised_hamming_distance, spread, pairwise_dispersion, 
                   bna, satisfiability_count, Position, 
                   aggregated_position_of_winners)

from statistics import mean
import numpy as np
import pandas as pd

def evaluate_experiment(*args, **dargs):
    """
    In taupy 0.4 and earlier, there wasn't an Evaluation class. All uses of this
    function can be adopted to the new class pretty easily. See the user guide
    for more information.
    """
    raise NotImplementedError(
        "This function is deprecated. Please use the Evaluation() class instead."
    )

class Evaluation():
    """
    A class to collect measurement values for a simulation while storing shared 
    information between evaluation functions (such as clusterings).
    
    :param debate_stages: An iterator containing the lists of debate stages for
        each simulation run.
    
    :param list_of_positions: An iterator containing the lists of belief sytems
        for each simulation run.
    
    :param clustering_method: When evaluation functions that rely on position
        clustering are called, the clustering algorithm specified here will be
        used. Functions from :py:mod:`taupy.analysis.clustering` can be selected
        here, in particular :py:func:`leiden`, :py:func:`affinity_propagation`,
        and :py:func:`agglomerative_clustering`.
    
    :param dict multiprocessing_settings: Settings forwarded to multiprocessing. 
        Should be options that are recognised by 
        :py:class:`concurrent.futures.ProcessPoolExecutor`.
    
    :var data: A :py:obj:`pandas.DataFrame` containing the analysed data.
    
    """
    def __init__(self, *, debate_stages, list_of_positions=None, 
                 clustering_method=None, multiprocessing_settings={}):
        self.simulations = debate_stages
        self.clustering_method = clustering_method
        self.positions = self.gather_positions(list_of_positions)
        self.data = pd.DataFrame()
        self.clusters = []
        self.mpsettings = multiprocessing_settings

    def __repr__(self):
        """
        Return the DataFrame when object is printed.
        """
        return repr(self.data)

    def gather_positions(self, position_location):
        if position_location == None:
            return [sim.positions for sim in self.simulations]
        else:
            return position_location

    def generate_clusters(self, *, clustering_settings={}):
        """
        Apply the clustering algorithm selected in 
        :py:attr:`Evaluation.clustering_method` to the stored debate stages and 
        positions. The clusters are saved in the :py:obj:`Evaluation.clusters` 
        list and can be accessed by functions that work on clusterings.
        """

        if self.clustering_method is None:
            raise ValueError("No clustering method found.")

        with ProcessPoolExecutor(**self.mpsettings) as executor:
            clustering_results = [executor.submit(
                                    obtain_clusterings,
                                    method=self.clustering_method,
                                    positions=i,
                                    settings=clustering_settings
                                    ) for i in self.positions]

        self.clusters = [i.result() for i in clustering_results]
        return 

    def add_data_columns(self, list_of_series):
        """
        Add measurements stored in a list of pd.Series to the DataFrame.
        """
        input_data = pd.DataFrame(
                        pd.concat(
                            list_of_series, 
                            keys=list(range(len(self.simulations)))
                            )
                        )
        self.data = pd.concat([self.data, input_data], axis=1)
        return

    def debate_stage_analysis(self, function):
        """
        A generic evaluation method to analyse, in multiprocessing, only debate
        stages without taking further data into account. From this module, 
        functions that can be passed to :py:attr:`function` are:

        - :py:func:`densities_of_debate_stages`
        - :py:func:`sccp_extension`
        - :py:func:`progress`
        """

        with ProcessPoolExecutor(**self.mpsettings) as executor:
            calculations = [executor.submit(
                                function, 
                                debate_stages=i
                                ) 
                            for i in self.simulations]

        observations = [i.result() for i in calculations]

        self.add_data_columns(observations)
        return

    def clusters_analysis(self, *, function, column_name="NAME",
                                 configuration={}):
        """
        Generic multi-process function to apply a measure that works on the 
        cluster structure of a simulation.
        
        :param function: A function to be applied in multiprocessing. 
            Here is a list of examples from different `taupy` 
            submodules that work with this function:

                - :py:func:`number_of_groups <taupy.analysis.polarisation.number_of_groups>`
                - :py:func:`group_size_parity <taupy.analysis.polarisation.group_size_parity>`
                - :py:func:`coverage_of_clustering <taupy.analysis.polarisation.coverage_of_clustering>`
                - :py:func:`Shannon_index <taupy.analysis.diversity.Shannon_index>`
                - :py:func:`normalised_Shannon_index <taupy.analysis.diversity.normalised_Shannon_index>`
                - :py:func:`Simpson_index <taupy.analysis.diversity.Simpson_index>`
                - :py:func:`inverse_Simpson_index <taupy.analysis.diversity.inverse_Simpson_index>`
                - :py:func:`Gini_Simpson_index <taupy.analysis.diversity.Gini_Simpson_index>`
        
            Note that :py:func:`group_divergence` and :py:func:`group_consensus`
            are calculated with dedicated methods. This is because both functions
            rely on additional information not present in the clustering alone.
        
        :param str column_name: Title of the column that is added to the 
            Evaluations :py:obj:`data` table. Should be indicative of the 
            measure that was applied.        
        """

        if len(self.clusters) != len(self.simulations):
            raise ValueError(
                "No suitable clustering found. Have you run generate_clusters()?"
            )
        
        with ProcessPoolExecutor(**self.mpsettings) as executor:
            clst = [executor.submit(
                    cluster_analysis,
                    function=function,
                    clusters=c,
                    column_name=column_name,
                    configuration=configuration
                    ) for c in self.clusters]

        observations = [i.result() for i in clst]

        self.add_data_columns(observations)
        return 

    def position_analysis(self, *, function, configuration={}):
        """
        A generic method to evaluate functions that work on positions, with
        multiprocessing. Examples are (see the shortcut functions as well):

        - :py:func:`dispersions_between_positions`
        - :py:func:`mean_agreement_between_positions`
        """

        with ProcessPoolExecutor(**self.mpsettings) as executor:
            observations = [executor.submit(
                    function,
                    positions=i,
                    **configuration
                    ) for i in self.positions]

        results = [i.result() for i in observations]        

        self.add_data_columns(results)
        return

    def densities(self):
        """
        A shortcut function to directly add the densities to the evaluation
        DataFrame.
        """
        return self.debate_stage_analysis(
                    function=densities_of_debate_stages
                    )

    def dispersions(self, *, configuration={}):
        """
        A shortcut function to directly add pairwise dispersion measurements to 
        the evaluation DataFrame.
        """
        return self.position_analysis(
                    function=dispersions_between_positions,
                    configuration=configuration
                    )

    def agreement_means(self, *, configuration={}):
        """
        A shortcut to directly add the mean population-wide agreement to the
        evaluation DataFrame.
        """
        return self.position_analysis(
                    function=mean_agreement_between_positions,
                    configuration=configuration
                    )

    def group_divergence(self, *, measure=normalised_hamming_distance):
        """
        Calculate the group divergence between all positions stored in the 
        :py:class:`Evaluation` object and add a column to the data object.
        Raises an error if no clustering has been generated. 
        
        See :py:func:`taupy.analysis.polarisation.group_divergence` for details.
        """

        if len(self.clusters) != len(self.simulations):
            raise ValueError(
                "No suitable clustering found. Have you run generate_clusters()?"
            )

        with ProcessPoolExecutor(**self.mpsettings) as executor:
            clst = [executor.submit(
                        divergencies_among_positions,
                        clusters=self.clusters[n],
                        measure=measure,
                        positions=i
                    ) for n, i in enumerate(self.positions)]
            
            results = [i.result() for i in clst]
        
        self.add_data_columns(results)
        return

    def group_consensus(self, *, measure=normalised_hamming_distance):
        """
        Calculate the group consensus between all positions stored in the 
        :py:class:`Evaluation` object and add a column to the data object.
        Raises an error if no clustering has been generated. 
        
        See :py:func:`taupy.analysis.polarisation.group_consensus` for details.
        """
        if len(self.clusters) != len(self.simulations):
            raise ValueError(
                "No suitable clustering found. Have you run generate_clusters()?"
            )

        with ProcessPoolExecutor(**self.mpsettings) as executor:
            clst = [executor.submit(
                        consensus_among_positions,
                        clusters=self.clusters[n],
                        measure=measure,
                        positions=i
                    ) for n, i in enumerate(self.positions)]
            
            results = [i.result() for i in clst]
        
        self.add_data_columns(results)
        return

    def coherence_of_majority_positions(self, *, not_present_value=None):

        with ProcessPoolExecutor(**self.mpsettings) as executor:
            calculations = [executor.submit(
                                majority_coherences,
                                positions=self.positions[i],
                                debate_stages=sim,
                                not_present_value=not_present_value
                                ) 
                            for i, sim in enumerate(self.simulations)]

        cmp = [i.result() for i in calculations]

        self.add_data_columns(cmp)
        return 

def densities_of_debate_stages(debate_stages):
    return pd.Series([i.density() for i in debate_stages], name="density")

def progress(debate_stages):
    return pd.Series(
            [i/(len(debate_stages)-1) for (i,_) in enumerate(debate_stages)], 
            name="progress"
            )

def dispersions_between_positions(positions, 
                                  *, 
                                  measure=normalised_hamming_distance):
    return pd.Series(
        [pairwise_dispersion(i, measure=measure) for i in positions],
        name="dispersion"
        )

def spread_between_positions(positions, 
                             *, 
                             measure=normalised_hamming_distance):
        
    return pd.Series(
            [spread(i, measure=measure) for i in positions], 
            name="spread"
            )

def mean_agreement_between_positions(positions, *, measure=bna):
    return pd.Series(
            [difference_matrix(i, measure=measure)[
                np.triu_indices(len(i), k=1)].mean() for i in positions],
            name="agreement"
            )

def majority_coherences(*, positions, debate_stages, not_present_value=None):
    return pd.Series([Position(
                        stage, 
                        aggregated_position_of_winners(
                            positions[i],
                            not_present_value=not_present_value
                        )
                    ).is_coherent() for (i,stage) in enumerate(debate_stages)],
                    name="majority is coherent"
                )

def numbers_of_unique_positions(positions):
    return pd.Series(
            [len([
                dict(i) for i in set(frozenset(position.items())
                                        for position in positions)
                ])
            ], 
            name="number of unique positions"
            )

def sccp_extension(debate_stages):
    return pd.Series(
            [satisfiability_count(i) for i in debate_stages], 
            name="Size of SCCP"
            ) 

def divergencies_among_positions(*, positions, clusters, 
                                 measure=normalised_hamming_distance):
    if len(clusters) != len(positions):
        raise ValueError(
            "The supplied clustering is unsuitable for the supplied positions."
        )
    
    matrices = [difference_matrix(i, measure=measure) for i in positions]
    return pd.Series(
            [group_divergence(i, matrices[num]) 
                for num, i in enumerate(clusters)],
            name="group divergence"
            )

def consensus_among_positions(*, positions, clusters, 
                              measure=normalised_hamming_distance):

    if len(clusters) != len(positions):
        raise ValueError(
            "The supplied clustering is unsuitable for the supplied positions."
        )
    
    matrices = [difference_matrix(i, measure=measure) for i in positions]
        
    return pd.Series(
            [group_consensus(i, matrices[num]) 
                for num, i in enumerate(clusters)],
            name="group consensus"
        )

def obtain_clusterings(*, method, positions, settings={}):
    """
    Apply the clustering method to the collection of positions stored in a 
    simulation.
    """
    return [method(i, **settings) for i in positions]

def cluster_analysis(*, function, clusters, column_name="NAME", 
                     configuration={}):
        """
        :param function: A function to work on the cluster structure.
        :param column_name: The column name in the parent Evaluation's DataFrame.

        A function that applies a measure on the cluster structure alone without
        further processing.
        """
        return pd.Series(
                [function(i, **configuration) for i in clusters],
                name=column_name
            )

def position_changes(*,
                     debate_stages, 
                     positions,
                     measure=normalised_hamming_distance
                     ):
    
    #pairs of debate stages
    p = [positions[i:i+2] for i in range(len(positions)-1)]
    averages = []
    
    for pair in p:
        d = [measure(pair[0][i], pair[1][i]) for i in range(len(pair[0]))]
        averages.append(len([pos for pos in d if pos != 0]))

    densities = [i.density() for i in debate_stages]
    density_pairs = [mean(densities[i:i+2]) for i in range(len(densities)-1)]
    
    return pd.DataFrame(list(zip(density_pairs, averages)), 
                                columns=["avg density in pair", 
                                         "position difference"])
