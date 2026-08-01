"""Behavioural tests for catalog.Catalog (current behaviour through S5).

Run: python test_catalog.py
Covers add/all/search, the four search() arguments (query, where, sort_by,
limit), copy-in/copy-out isolation, and the policies recorded in
docs/ssot/DECISIONS.md. Per S5 (D9), a `where` key missing from an item is
treated as a non-match (no ValueError); a key absent from every item yields [].
"""

import copy

from catalog import Catalog


def names(items):
    return [i["name"] for i in items]


def make_basic():
    c = Catalog()
    c.add({"name": "Apple", "color": "red", "qty": 3})
    c.add({"name": "banana", "color": "yellow", "qty": 1})
    c.add({"name": "Cherry", "color": "red", "qty": 2})
    return c


# --- add / all / insertion order (D3) -------------------------------------

def test_all_insertion_order():
    c = make_basic()
    assert names(c.all()) == ["Apple", "banana", "Cherry"]


def test_no_arg_search_equals_all():
    c = make_basic()
    assert c.search() == c.all()
    assert names(c.search()) == ["Apple", "banana", "Cherry"]


# --- copy in / copy out isolation (D1) ------------------------------------

def test_add_copies_in():
    c = Catalog()
    src = {"name": "X", "tags": ["a"]}
    c.add(src)
    src["name"] = "MUTATED"
    src["tags"].append("b")
    out = c.all()[0]
    assert out["name"] == "X"
    assert out["tags"] == ["a"]


def test_all_copies_out():
    c = make_basic()
    got = c.all()
    got[0]["name"] = "MUTATED"
    got[0]["color"] = "green"
    assert names(c.all()) == ["Apple", "banana", "Cherry"]
    assert c.all()[0]["color"] == "red"


def test_search_copies_out():
    c = make_basic()
    got = c.search(query="apple")
    got[0]["name"] = "MUTATED"
    assert names(c.search(query="apple")) == ["Apple"]


# --- query: case-insensitive substring on name (D4 matching half) ---------

def test_query_substring_case_insensitive():
    c = make_basic()
    assert names(c.search(query="err")) == ["Cherry"]
    assert names(c.search(query="A")) == ["Apple", "banana"]  # 'A' in Apple/banana
    assert names(c.search(query="APPLE")) == ["Apple"]


def test_query_keeps_insertion_order():
    c = Catalog()
    c.add({"name": "ba"})
    c.add({"name": "ab"})
    c.add({"name": "Xa"})
    assert names(c.search(query="a")) == ["ba", "ab", "Xa"]


def test_query_no_match_empty():
    c = make_basic()
    assert c.search(query="zzz") == []


def test_query_none_is_list_mode():
    c = make_basic()
    assert names(c.search(query=None)) == ["Apple", "banana", "Cherry"]


# --- blank/whitespace query -> [] (D6, supersedes D4 blank half) ----------

def test_query_blank_returns_empty():
    c = make_basic()
    assert c.search(query="") == []
    assert c.search(query="   ") == []
    assert c.search(query="\t\n") == []


# --- where: equality + AND (D5), missing key -> no match (D9, S5) ---------

def test_where_single_key():
    c = make_basic()
    assert names(c.search(where={"color": "red"})) == ["Apple", "Cherry"]


def test_where_multi_key_and():
    c = make_basic()
    assert names(c.search(where={"color": "red", "qty": 2})) == ["Cherry"]
    # tightening the value drops the other red item
    assert names(c.search(where={"color": "red", "qty": 99})) == []


def test_where_no_match_empty():
    c = make_basic()
    assert c.search(where={"color": "green"}) == []


def test_where_empty_dict_lists_all():
    c = make_basic()
    assert names(c.search(where={})) == ["Apple", "banana", "Cherry"]


def test_where_composes_with_query():
    c = make_basic()
    # query 'a' -> Apple, banana; where red -> Apple
    assert names(c.search(query="a", where={"color": "red"})) == ["Apple"]


def test_where_key_missing_from_all_returns_empty():
    # S5 / D9: no ValueError; a key on no item matches nothing -> [].
    c = make_basic()
    assert c.search(where={"size": "big"}) == []


def test_where_key_missing_from_some_filters_those_out():
    # S5 / D9: items lacking the key are non-matches (dropped), not errors.
    c = Catalog()
    c.add({"name": "withkey", "tag": "x"})
    c.add({"name": "nokey"})  # no 'tag'
    c.add({"name": "withkey2", "tag": "x"})
    assert names(c.search(where={"tag": "x"})) == ["withkey", "withkey2"]


def test_where_missing_key_composes_with_query():
    # missing-key non-match still composes with query filtering.
    c = Catalog()
    c.add({"name": "alpha", "tag": "x"})
    c.add({"name": "alpine"})  # matches query 'alp' but lacks 'tag'
    assert names(c.search(query="alp", where={"tag": "x"})) == ["alpha"]


# --- sort_by: ascending, stable, missing-key/type policy (D7) -------------

def test_sort_by_ascending():
    c = make_basic()
    assert names(c.search(sort_by="qty")) == ["banana", "Cherry", "Apple"]


def test_sort_by_is_stable():
    c = Catalog()
    c.add({"name": "first", "k": 1})
    c.add({"name": "second", "k": 1})
    c.add({"name": "third", "k": 0})
    # k=1 ties keep insertion order (first before second)
    assert names(c.search(sort_by="k")) == ["third", "first", "second"]


def test_sort_after_filtering():
    c = make_basic()
    # where red -> Apple(3), Cherry(2); sorted by qty asc -> Cherry, Apple
    assert names(c.search(where={"color": "red"}, sort_by="qty")) == ["Cherry", "Apple"]


def test_sort_missing_key_raises():
    c = make_basic()
    try:
        c.search(sort_by="weight")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for sort_by missing on items")


def test_sort_incomparable_types_raise():
    c = Catalog()
    c.add({"name": "a", "k": 1})
    c.add({"name": "b", "k": "str"})
    try:
        c.search(sort_by="k")
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError for incomparable sort values")


# --- limit: top N after sort, edge cases (D8) -----------------------------

def test_limit_caps_results():
    c = make_basic()
    assert names(c.search(limit=2)) == ["Apple", "banana"]


def test_limit_top_n_after_sort():
    c = make_basic()
    # sort by qty asc -> banana(1), Cherry(2), Apple(3); top 2
    assert names(c.search(sort_by="qty", limit=2)) == ["banana", "Cherry"]


def test_full_pipeline_query_where_sort_limit():
    c = Catalog()
    c.add({"name": "red-apple", "color": "red", "qty": 5})
    c.add({"name": "red-rose", "color": "red", "qty": 2})
    c.add({"name": "red-rug", "color": "red", "qty": 9})
    c.add({"name": "blue-rug", "color": "blue", "qty": 1})
    # query 'r' (all names contain 'r') -> where red -> 3 items
    # sort by qty asc -> rose(2), apple(5), rug(9); limit 2 -> rose, apple
    got = c.search(query="r", where={"color": "red"}, sort_by="qty", limit=2)
    assert names(got) == ["red-rose", "red-apple"]


def test_limit_zero_empty():
    c = make_basic()
    assert c.search(limit=0) == []


def test_limit_at_or_above_count_returns_all():
    c = make_basic()
    assert names(c.search(limit=3)) == ["Apple", "banana", "Cherry"]
    assert names(c.search(limit=100)) == ["Apple", "banana", "Cherry"]


def test_limit_negative_raises():
    c = make_basic()
    try:
        c.search(limit=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for negative limit")


def test_limit_non_int_raises():
    c = make_basic()
    for bad in (1.0, "1", [1]):
        try:
            c.search(limit=bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for limit={bad!r}")


def test_limit_bool_raises():
    c = make_basic()
    for bad in (True, False):
        try:
            c.search(limit=bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for limit={bad!r}")


def test_limit_none_no_cap():
    c = make_basic()
    assert names(c.search(limit=None)) == ["Apple", "banana", "Cherry"]


def test_search_does_not_mutate_internal_state():
    c = make_basic()
    before = c.all()
    c.search(query="a", where={"color": "red"}, sort_by="qty", limit=1)
    assert c.all() == before


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        t()
        passed += 1
    print(f"{passed} tests passed")


if __name__ == "__main__":
    _run()
