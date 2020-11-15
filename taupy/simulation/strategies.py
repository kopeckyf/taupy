"""
Argument input strategies, defined in dictionary mappings
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