# rank — R2 policy: score DESC, ties broken REVERSE-ALPHABETICAL (descending)
def rank(scores):
    items = list(scores.items())
    items.sort(key=lambda kv: kv[0], reverse=True)    # reverse alpha
    items.sort(key=lambda kv: kv[1], reverse=True)     # score desc (stable)
    return [k for k, _ in items]
