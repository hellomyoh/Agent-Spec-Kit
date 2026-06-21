def rank(scores: dict) -> list:
    """
    Rank names by score in descending order, with tie-breaking by name length then alphabetically.

    Args:
        scores: Dictionary mapping names (str) to scores (int)

    Returns:
        List of names ordered by score (descending), then by length (ascending),
        then alphabetically (A→Z) for ties with the same score and length

    Examples:
        rank({"x":5,"y":9,"z":1}) == ["y","x","z"]
        rank({"ab":10,"ba":10,"abc":10}) == ["ab","ba","abc"]
    """
    return sorted(scores.keys(), key=lambda name: (-scores[name], len(name), name))
