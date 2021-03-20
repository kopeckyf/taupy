"""
The following argumentation strategies are pre-defined in taupy. They all
introduce arguments that are valid given the current debate stage.

:py:obj:`random`
    A completely random strategy that works even if a simulation has no
    positions at all.

:py:obj:`fortify`
    Insert a valid argument the premises and conclusion of which are accepted
    by the source position.

:py:obj:`attack`
    A valid argument. The premises are accepted by the source position, and
    the source at least tolerates the conclusion. However, the target denies 
    the conclusion, given its current truth-value attribution.

:py:obj:`convert`
    A valid argument with premises picked from the target. The conclusion is 
    picked from the source, and the source also accepts the conclusion. It is
    not checked whether the target accepts the conclusion.

:py:obj:`undercut`
    A valid argument is constructed with premises that the target accepts. The
    source at least tolerates the conclusion. The conclusion however is not 
    accepted by the target.
"""

random = {"source": False,
          "target": False,
          "pick_premises_from": None,
          "source_accepts_conclusion": "NA",
          "target_accepts_conclusion": "NA",
          "name": "random"}

fortify = {"source": True,
           "target": False,
           "pick_premises_from": "source",
           "source_accepts_conclusion": "Yes",
           "target_accepts_conclusion": "NA",
           "name": "fortify"}

attack = {"source": True,
          "target": True,
          "pick_premises_from": "source",
          "source_accepts_conclusion": "Toleration",
          "target_accepts_conclusion": "No",
          "name": "attack"}

convert = {"source": True,
           "target": True,
           "pick_premises_from": "target",
           "source_accepts_conclusion": "Yes",
           "target_accepts_conclusion": "NA",
           "name": "convert"}

undercut = {"source": True,
            "target": True,
            "pick_premises_from": "target",
            "source_accepts_conclusion": "Toleration",
            "target_accepts_conclusion": "No",
            "name": "undercut"}
