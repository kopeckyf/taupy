"""
taupy is a Python 3 library for the theory of dialectical structures.
"""

from .basic import Argument, Debate, EmptyDebate
from .basic import (Position, position_compatibility, closedness)
from .basic import (satisfiability_count, satisfiability, dict_to_prop, 
                    dict_to_binary, pick_random_positions_from_debate,
                    free_premises, graph_from_positions, ari,
                    subsequences_with_length, satisfiable_extensions, fetch_premises,
                    proposition_levels_from_debate, select_premises, fetch_conclusion)

from .analysis import (doj, hamming_distance, normalised_hamming_distance, bna, next_neighbours, 
                       edit_distance, normalised_edit_distance, switch_deletion_neighbourhood,
                       groups_from_stance_toward_single_proposition,
                       difference_matrix, spread, lauka, number_of_groups,
                       pairwise_dispersion, group_divergence, group_consensus, group_size_parity)

from .simulation import (Simulation, experiment, introduce, response, 
                         evaluate_experiment)

__all__ = [
            # Core ontology
            'Argument', 'Debate', 'EmptyDebate', 'Position', 
            'position_compatibility', 'closedness',
            # .analysis
            'doj', 'hamming_distance', 'normalised_hamming_distance', 
            'bna', 'next_neighbours', 'edit_distance', 'normalised_edit_distance',
            'switch_deletion_neighbourhood',
            'groups_from_stance_toward_single_proposition', 'number_of_groups',
            'difference_matrix', 'spread', 'lauka', 'pairwise_dispersion',
            'group_divergence', 'group_consensus', 'group_size_parity',
            # .simulation
            'Simulation', 'experiment',
            'evaluate_experiment',
            # Update mechanisms
            'introduce', 'response',
            # Common utilities
            'satisfiability_count', 'satisfiability', 'dict_to_prop',
            'dict_to_binary', 'pick_random_positions_from_debate',
            'free_premises', 'graph_from_positions', 'ari', 
            'subsequences_with_length', 'satisfiable_extensions', 'fetch_premises',
            'proposition_levels_from_debate', 'fetch_conclusion', 'select_premises'
          ]
