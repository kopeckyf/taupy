"""
Argument input strategies, defined in dictionary mappings
"""

random = {"source": False,
          "target": False,
          "pick_premises_from": None,
          "pick_conclusion_from": None,
          "source_accepts_conclusion": "NA",
          "target_accepts_conclusion": "NA"}

fortify = {"source": True,
           "target": False,
           "pick_premises_from": "source",
           "pick_conclusion_from": "source",
           "source_accepts_conclusion": True,
           "target_accepts_conclusion": "NA"}

attack = {"source": True,
          "target": True,
          "pick_premises_from": "source",
          "pick_conclusion_from": "target",
          "source_accepts_conclusion": "Toleration",
          "target_accepts_conclusion": False}

convert = {"source": True,
           "target": True,
           "pick_premises_from": "target",
           "pick_conclusions_from": "source",
           "source_accepts_conclusion": True,
           "target_accepts_conclusion": "NA"}

undercut = {"source": True,
            "target": True,
            "pick_premises_from": "target",
            "pick_conclusions_from": None,
            "source_accepts_conclusion": "Toleration",
            "target_accepts_conclusion": False}
