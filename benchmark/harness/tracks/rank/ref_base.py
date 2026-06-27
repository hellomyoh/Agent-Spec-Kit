# rank — BASE policy: score DESC, ties broken ALPHABETICAL ascending
def rank(scores):
    items = list(scores.items())
    items.sort(key=lambda kv: kv[0])               # alpha asc
    items.sort(key=lambda kv: kv[1], reverse=True)  # score desc (stable)
    return [k for k, _ in items]
