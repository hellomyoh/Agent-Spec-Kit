def rank(scores: dict) -> list:
    """
    Rank names by score, with ties broken by length (ascending) then alphabetical order.

    Args:
        scores: Dictionary mapping name (str) to score (int)

    Returns:
        List of names sorted by score (descending), then by length (ascending), then by name (alphabetical, A→Z)
    """
    return sorted(scores.keys(), key=lambda name: (-scores[name], len(name), name))
