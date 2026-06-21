# rank — R1 policy: score DESC, ties broken by NAME LENGTH ascending, then alphabetical
def rank(scores):
    items = list(scores.items())
    items.sort(key=lambda kv: (len(kv[0]), kv[0]))   # length asc, then alpha
    items.sort(key=lambda kv: kv[1], reverse=True)    # score desc (stable)
    return [k for k, _ in items]
