# rank hidden tests. get_core() = invariants true for ALL policies (P2P).
# get_policy(name) = the tie-break behavior specific to base/R1/R2.
TIE = {"ab": 10, "ba": 10, "abc": 10}
TIE2 = {"zzz": 7, "yy": 7, "x": 7, "w": 1}

def get_core():
    def all_present(sol):
        assert sorted(sol.rank({"a": 3, "b": 1, "c": 2})) == ["a", "b", "c"]
    def desc_distinct(sol):
        assert sol.rank({"x": 5, "y": 9, "z": 1}) == ["y", "x", "z"]
    def desc_distinct2(sol):
        assert sol.rank({"p": 2, "q": 8, "r": 5}) == ["q", "r", "p"]
    def empty(sol):
        assert sol.rank({}) == []
    return [("all_present", all_present), ("desc_distinct", desc_distinct),
            ("desc_distinct2", desc_distinct2), ("empty", empty)]

def get_policy(name):
    exp = {"base": ["ab", "abc", "ba"], "R1": ["ab", "ba", "abc"], "R2": ["ba", "abc", "ab"]}[name]
    exp2 = {"base": ["x", "yy", "zzz", "w"], "R1": ["x", "yy", "zzz", "w"], "R2": ["zzz", "yy", "x", "w"]}[name]
    def tie(sol):
        got = sol.rank(dict(TIE)); assert got == exp, f"got {got} want {exp}"
    def tie2(sol):
        got = sol.rank(dict(TIE2)); assert got == exp2, f"got {got} want {exp2}"
    return [("tie", tie), ("tie2", tie2)]
