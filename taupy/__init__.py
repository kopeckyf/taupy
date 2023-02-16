"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from .basic import Argument, Debate, EmptyDebate
from .basic import (Position, position_compatibility, closedness)
from .basic import (satisfiability_count, satisfiability, dict_to_prop, 
                    dict_to_binary, pick_random_positions_from_debate,
                    free_premises, graph_from_positions, ari,
                    subsequences_with_length, satisfiable_extensions, fetch_premises,
                    proposition_levels_from_debate, premise_usage_count,
                    select_premises, fetch_conclusion,
                    z3_assertion_from_argument, z3_soft_constraints_from_position,
                    z3_all_models)

from .analysis import (doj, hamming_distance, normalised_hamming_distance, bna, next_neighbours, 
                       edit_distance, normalised_edit_distance, switch_deletion_neighbourhood,
                       groups_from_stance_toward_single_proposition,
                       difference_matrix, spread, lauka, number_of_groups,
                       pairwise_dispersion, group_divergence, group_consensus, group_size_parity,
                       normalised_edit_agreement, aggregated_position_of_winners,
                       attribute_diversity_page, Gini_Simpson_index, 
                       inverse_Simpson_index, normalised_attribute_diversity_page,
                       normalised_Shannon_index, Shannon_index, Simpson_index,
                       ncc, average_ncc, clustering_matrix, leiden, affinity_propagation,
                       agglomerative_clustering, density_based_clustering)

from .simulation import (Simulation, FixedDebateSimulation, 
                         SocialInfluenceSimulation,
                         experiment, introduce, response,
                         strategies, 
                         Evaluation, evaluate_experiment)

from .generators import generate_hierarchical_argument_map

__all__ = [
            # Core ontology
            'Argument', 'Debate', 'EmptyDebate', 'Position', 
            'position_compatibility', 'closedness',
            # .analysis
            'doj', 
            'attribute_diversity_page', 'Gini_Simpson_index', 
            'inverse_Simpson_index', 'normalised_attribute_diversity_page',
            'normalised_Shannon_index', 'Shannon_index', 'Simpson_index',
            'hamming_distance', 'normalised_hamming_distance', 
            'bna', 'next_neighbours', 'edit_distance', 'normalised_edit_distance',
            'switch_deletion_neighbourhood', 'normalised_edit_agreement',
            'groups_from_stance_toward_single_proposition', 'number_of_groups',
            'difference_matrix', 'spread', 'lauka', 'pairwise_dispersion',
            'group_divergence', 'group_consensus', 'group_size_parity',
            'aggregated_position_of_winners', 'ncc', 'average_ncc',
            'clustering_matrix', 'leiden', 'affinity_propagation', 
            'agglomerative_clustering', 'density_based_clustering',
            # .simulation
            'Simulation', 'FixedDebateSimulation', 'SocialInfluenceSimulation',
            'experiment', 'Evaluation', 'evaluate_experiment', 'strategies',
            # Update mechanisms
            'introduce', 'response',
            # Common utilities
            'satisfiability_count', 'satisfiability', 'dict_to_prop',
            'dict_to_binary', 'pick_random_positions_from_debate',
            'free_premises', 'graph_from_positions', 'ari', 
            'subsequences_with_length', 'satisfiable_extensions', 'fetch_premises',
            'proposition_levels_from_debate', 'premise_usage_count',
            'fetch_conclusion', 'select_premises',
            'z3_assertion_from_argument', 'z3_soft_constraints_from_position',
            'z3_all_models',
            # Generators
            'generate_hierarchical_argument_map'
          ]
