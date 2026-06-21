# clean_tags — R1 policy: same cleaning, output SORTED ALPHABETICAL ascending
def _clean(tags):
    out, seen = [], set()
    for t in tags:
        s = t.strip().lower()
        if not s or s in seen:
            continue
        seen.add(s); out.append(s)
    return out

def clean_tags(tags):
    return sorted(_clean(tags))            # alphabetical
