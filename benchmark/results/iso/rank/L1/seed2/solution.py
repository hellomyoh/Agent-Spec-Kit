def rank(scores: dict) -> list:
    """
    Return names ordered by score descending, with length-then-alphabetical tie-breaking.

    Args:
        scores: dict {name: score(int)} -> list of names

    Returns:
        list of names ordered by score descending, ties broken by name length ascending then alphabetically ascending
    """
    return sorted(scores.keys(), key=lambda name: (-scores[name], len(name), name))
