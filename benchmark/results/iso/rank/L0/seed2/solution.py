def rank(scores: dict) -> list:
    return [name for name, _ in sorted(scores.items(), key=lambda x: (-x[1], x[0]))]
