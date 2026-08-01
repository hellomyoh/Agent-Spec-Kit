def rank(scores: dict) -> list:
    return [name for name, _ in sorted(scores.items(), key=lambda item: (-item[1], len(item[0]), item[0]))]
