# clean_tags hidden tests. core = cleaning invariants (order-independent, all policies).
# policy = output ordering specific to base/R1/R2.
RAW = ["Banana", "apple", "Fig", " apple ", "cc", ""]

def get_core():
    def cleaned_set(sol):
        r = sol.clean_tags(list(RAW))
        assert set(r) == {"banana", "apple", "fig", "cc"} and len(r) == 4
    def lower_strip(sol):
        assert sol.clean_tags(["  HELLO  "]) == ["hello"]
    def dedup_count(sol):
        assert len(sol.clean_tags(["a", "A", "a "])) == 1
    def drop_empty(sol):
        assert sol.clean_tags(["", "   ", "x"]) == ["x"]
    return [("cleaned_set", cleaned_set), ("lower_strip", lower_strip),
            ("dedup_count", dedup_count), ("drop_empty", drop_empty)]

def get_policy(name):
    exp = {"base": ["banana", "apple", "fig", "cc"],
           "R1": ["apple", "banana", "cc", "fig"],
           "R2": ["cc", "fig", "apple", "banana"]}[name]
    def order(sol):
        got = sol.clean_tags(list(RAW)); assert got == exp, f"got {got} want {exp}"
    return [("order", order)]
