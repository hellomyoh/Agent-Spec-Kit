def rank(scores: dict) -> list:
    from functools import cmp_to_key
    def compare(item1, item2):
        name1, score1 = item1
        name2, score2 = item2
        if score1 != score2:
            return score2 - score1
        return -1 if name1 < name2 else (1 if name1 > name2 else 0)
    return [name for name, _ in sorted(scores.items(), key=cmp_to_key(compare))]
