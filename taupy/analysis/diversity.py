"""
Functions to measure diversity among deliberating agents. Interestingly, many
functions in the module have a common abstract ancestor function (Tuomisto 2010), 
but are implemented here in a rather pedestrian way for simplicty.


------
References:
Tuomisto, Hanna. 2010. A consistent terminology for quantifying species 
diversity? Yes, it does exist. Oecologia 164: 853–860. DOI: 10/c445xk.
"""

from .polarisation import number_of_groups
from math import log

def Shannon_index(clusters):
    """
    The Shannon index describes the uncertainty of predicting the cluster
    that the belief system of a randomly drawn agent belongs to.

    (Note that math.log defaults to base e, and so returns ln here – although
    sometimes a different base is used for the Shannon index.)
    """
    clusters = [c for c in clusters if c]

    population_size = sum([len(c) for c in clusters])
    return  -1 * sum([len(c)/population_size * log(
            len(c)/population_size) for c in clusters])

def normalised_Shannon_index(clusters):

    clusters = [c for c in clusters if c]

    return Shannon_index(clusters) / log(number_of_groups(clusters))

def Simpson_index(clusters):
    """
    The Simpson index of diversity equals the probability that the belief
    systems of two randomly chosen agents belong to the same cluster.
    """
    clusters = [c for c in clusters if c]
    population_size = sum([len(c) for c in clusters])

    return sum([(len(c)/population_size)**2 for c in clusters])

def inverse_Simpson_index(clusters):
    """
    Simpson's inverse index is simply dubbed “diversity index” in Page's 
    “Diversity and complexity”. Political scientists call it “effective 
    number of parties”, and economists know it as Herfindahl index.
    ------
    References:

    Page, Scott E. 2011. Diversity and complexity. 
    Princeton University Press, pp. 73–76.

    Laakso, Markku & Taagepera, Rein. 1979. “Effective” number of parties: 
    A measure with application to West Europe. Comparative Political Studies 
    12(1): 3–27.
    """

    return 1 / Simpson_index(clusters)

def Gini_Simpson_index(clusters):
    """
    Estimates the probability that the belief systems of two randomly drawn
    agents are clustered into different clusters (“inter-type encounters”). 
    """
    return 1 - Simpson_index(clusters)

def attribute_diversity_page(positions):
    """
    Page's attribute diversity is equal to the number of distinct attributes
    in the population. We interpret it to count the number of distinct truth-
    value attributions: a population in which both {p1: True} and {p1: False}
    are maintained is more diverse then a population in which just {p1: True}
    is maintained.
    ------
    References:

    Page, Scott E. 2011. Diversity and complexity. 
    Princeton University Press, pp. 73–76.
    """
    attributes = set()

    for pos in positions:
        attributes |= pos.items()

    return len(attributes)

def normalised_attribute_diversity_page(positions,
                                        sentencepool,
                                        truth_values=[True, False]):
    """
    Page's attribute diversity, normalised to the amount of truth-value
    attributions possible without any constraints (number of sentences * 
    allowed truth values). This normalised diversity measure is not weighted,
    since all attributes contribute to it equally.
    """
    max_attribute_diversity = len(sentencepool) * len(truth_values)

    return attribute_diversity_page(positions) / max_attribute_diversity