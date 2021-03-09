"""
Argument input strategies, defined in dictionary mappings. These strategies are
defined in Betz 2013: Table 6.1.

References
----------
Betz, Gregor. 2013. Debate dynamics: How controversy improves our beliefs. 
Springer. DOI: 10/d3cx
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
