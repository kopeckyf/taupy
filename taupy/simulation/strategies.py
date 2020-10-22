"""
Argument input strategies, defined in dictionary mappings
"""

fortify = {"source": True,
           "target": False,
           "premises_from": "source",
           "conclusion_from": "source",
           "target_accepts_conclusion": "Irrelevant"}

attack = {"source": True,
          "target": True,
          "premises_from": "source",
          "conclusion_from": "target",
          "target_accepts_conclusion": "No"}

convert = {"source": True,
           "target": True,
           "premises_from": "target",
           "conclusions_from": "source",
           "target_accepts_conclusion": "Yes"}

undercut = {"source": True,
            "target": True,
            "premises_from": "target",
            "conclusions_from": "source",
            "target_accepts_conclusion": "No"}
