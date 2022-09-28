def survey(p, *, positions, not_present_value=None):
    """
    Take a survey about proposition `p` among `positions`. This function is
    agnostic about truth values attributed to `p`. These could be True and False
    assuming a two-valued logic. If any position does not pass a judgement on 
    `p`, they respond `not_present_value` to the survey.
    """
    v = {}

    for pos in positions:
        if p not in pos:
            if not_present_value in v:
                v[not_present_value] += 1
            else:
                v[not_present_value] = 1
        else:
            if pos[p] in v:
                v[pos[p]] += 1
            else:
                v[pos[p]] = 1

    return v


def majority_vote_winner(p, *, positions, not_present_value=None):
    """
    Cast a simple majority vote about `p` among `positions` and return the 
    winner. This function checks whether the winner would be unique. A value 
    error is returned if no winner can be determined due to a tie.
    """

    s = survey(p, positions=positions, not_present_value=not_present_value)

    if len(s.values()) > 1 and sorted(s.values())[-1] == sorted(s.values())[-2]:
        # There is an equal number of votes for at least two options.
        # No majority voting winner can be determined.
        raise ValueError(
            f"The vote among input positions about {p} resulted in a tie."
        )

    # After uniqueness of winner is checked, return stance with maximum value.
    # (dict.items() returns key-value pairs of options and their popularity)
    return max(s.items(), key=lambda i: i[1])


def aggregated_position_of_winners(positions, *, not_present_value=None):
    """
    Return a Position that is aggregated from the input positions by majority
    voting.
    """
    propositions = set()
    # Iteratively build the union of coverages of the positions
    for p in positions:
        propositions = propositions | set(p.keys())

    return {p: majority_vote_winner(
                    p,
                    positions=positions,
                    not_present_value=not_present_value
                )[0] for p in propositions}