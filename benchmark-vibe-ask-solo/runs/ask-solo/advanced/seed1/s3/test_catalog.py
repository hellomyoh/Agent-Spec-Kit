"""Behavioural tests for catalog.Catalog (run: python test_catalog.py).

Covers the current behaviour pinned by docs/ssot: copy in/out (D1), insertion
order (D3), query substring + None-vs-blank handling (D4/D6), where equality
with AND and missing-key ValueError (D5), sort_by ascending/stable + missing-key
ValueError (D7), and limit still raising NotImplementedError (D2).
"""

import copy
from catalog import Catalog


def _names(items):
    return [i["name"] for i in items]


def make_catalog(*names):
    c = Catalog()
    for n in names:
        c.add({"name": n})
    return c


# --- add / all / copy isolation (D1, D3) ---

def test_all_returns_insertion_order():
    c = make_catalog("b", "a", "c")
    assert _names(c.all()) == ["b", "a", "c"]


def test_add_copies_in_source_mutation_isolated():
    c = Catalog()
    src = {"name": "x", "tags": ["t1"]}
    c.add(src)
    src["name"] = "MUT"
    src["tags"].append("t2")
    assert _names(c.all()) == ["x"]
    assert c.all()[0]["tags"] == ["t1"]


def test_all_copies_out_returned_mutation_isolated():
    c = make_catalog("x")
    got = c.all()
    got[0]["name"] = "MUT"
    got[0]["new"] = 1
    assert _names(c.all()) == ["x"]
    assert "new" not in c.all()[0]


def test_search_copies_out():
    c = make_catalog("x")
    got = c.search()
    got[0]["name"] = "MUT"
    assert _names(c.search()) == ["x"]


# --- no-argument search == all() (D3) ---

def test_search_no_args_lists_all_in_order():
    c = make_catalog("b", "a", "c")
    assert _names(c.search()) == ["b", "a", "c"]


def test_search_query_none_is_list_mode():
    # Contract: query=None means no text filter (list mode).
    c = make_catalog("b", "a", "c")
    assert _names(c.search(query=None)) == ["b", "a", "c"]


# --- query substring matching (D4) ---

def test_query_case_insensitive_substring():
    c = make_catalog("Banana", "apple", "Cherry", "avocado")
    assert _names(c.search(query="A")) == ["Banana", "apple", "avocado"]


def test_query_keeps_insertion_order_among_matches():
    c = make_catalog("aXa", "ba", "Ca")
    assert _names(c.search(query="a")) == ["aXa", "ba", "Ca"]


def test_query_no_match_is_empty():
    c = make_catalog("a", "b")
    assert c.search(query="zzz") == []


# --- blank query safety policy (D6, supersedes D4 blank handling) ---

def test_query_empty_string_returns_empty():
    c = make_catalog("a", "b", "c")
    assert c.search(query="") == []


def test_query_whitespace_only_returns_empty():
    c = make_catalog("a", "b", "c")
    assert c.search(query="   ") == []
    assert c.search(query="\t\n ") == []


# --- where equality filtering (D5) ---

def test_where_single_key_match():
    c = Catalog()
    c.add({"name": "a", "color": "red"})
    c.add({"name": "b", "color": "blue"})
    assert _names(c.search(where={"color": "red"})) == ["a"]


def test_where_multi_key_and():
    c = Catalog()
    c.add({"name": "a", "color": "red", "size": "L"})
    c.add({"name": "b", "color": "red", "size": "S"})
    assert _names(c.search(where={"color": "red", "size": "S"})) == ["b"]


def test_where_no_match_is_empty():
    c = Catalog()
    c.add({"name": "a", "color": "red"})
    c.add({"name": "b", "color": "blue"})
    assert c.search(where={"color": "green"}) == []


def test_where_empty_dict_lists_all():
    c = Catalog()
    c.add({"name": "a", "color": "red"})
    c.add({"name": "b", "color": "blue"})
    assert _names(c.search(where={})) == ["a", "b"]


def test_where_key_missing_on_all_raises():
    c = make_catalog("a", "b")
    try:
        c.search(where={"color": "red"})
    except ValueError:
        return
    raise AssertionError("expected ValueError for where key missing on all items")


def test_where_key_missing_on_some_raises():
    c = Catalog()
    c.add({"name": "a", "color": "red"})
    c.add({"name": "b"})  # missing 'color'
    try:
        c.search(where={"color": "red"})
    except ValueError:
        return
    raise AssertionError("expected ValueError for where key missing on some items")


def test_where_composes_with_query():
    c = Catalog()
    c.add({"name": "red apple", "color": "red"})
    c.add({"name": "red berry", "color": "red"})
    c.add({"name": "green apple", "color": "green"})
    assert _names(c.search(query="apple", where={"color": "red"})) == ["red apple"]


# --- sort_by ascending + stable (D7) ---

def test_sort_by_ascending():
    c = Catalog()
    c.add({"name": "c", "rank": 3})
    c.add({"name": "a", "rank": 1})
    c.add({"name": "b", "rank": 2})
    assert _names(c.search(sort_by="rank")) == ["a", "b", "c"]


def test_sort_by_is_stable_for_equal_keys():
    c = Catalog()
    c.add({"name": "x", "rank": 2})
    c.add({"name": "y", "rank": 1})
    c.add({"name": "z", "rank": 2})
    # equal rank (x, z) must preserve insertion order
    assert _names(c.search(sort_by="rank")) == ["y", "x", "z"]


def test_sort_by_applies_after_query_filter():
    c = Catalog()
    c.add({"name": "Apple", "rank": 3})
    c.add({"name": "Banana", "rank": 1})
    c.add({"name": "Apricot", "rank": 2})
    # query 'ap' keeps Apple, Apricot (not Banana); then sort by rank ascending
    assert _names(c.search(query="ap", sort_by="rank")) == ["Apricot", "Apple"]


def test_sort_by_applies_after_where_filter():
    c = Catalog()
    c.add({"name": "a", "color": "red", "rank": 2})
    c.add({"name": "b", "color": "blue", "rank": 1})
    c.add({"name": "c", "color": "red", "rank": 1})
    assert _names(c.search(where={"color": "red"}, sort_by="rank")) == ["c", "a"]


def test_sort_by_missing_key_raises_valueerror():
    c = Catalog()
    c.add({"name": "a", "rank": 1})
    c.add({"name": "b"})  # missing 'rank'
    try:
        c.search(sort_by="rank")
    except ValueError:
        return
    raise AssertionError("expected ValueError for sort_by key missing on a result item")


def test_sort_by_incomparable_types_raises_typeerror():
    c = Catalog()
    c.add({"name": "a", "v": 1})
    c.add({"name": "b", "v": "x"})
    try:
        c.search(sort_by="v")
    except TypeError:
        return
    raise AssertionError("expected TypeError for incomparable sort_by values")


def test_sort_by_does_not_mutate_internal_order():
    c = Catalog()
    c.add({"name": "c", "rank": 3})
    c.add({"name": "a", "rank": 1})
    c.search(sort_by="rank")
    # internal insertion order unchanged after a sorted search
    assert _names(c.all()) == ["c", "a"]


# --- limit still unspecified (D2) ---

def test_limit_raises_not_implemented():
    c = make_catalog("a", "b")
    try:
        c.search(limit=1)
    except NotImplementedError:
        return
    raise AssertionError("expected NotImplementedError for limit")


def test_limit_with_query_raises_not_implemented():
    c = make_catalog("a", "b")
    try:
        c.search(query="a", limit=1)
    except NotImplementedError:
        return
    raise AssertionError("expected NotImplementedError for query+limit")


def test_limit_with_sort_by_raises_not_implemented():
    c = Catalog()
    c.add({"name": "a", "rank": 1})
    try:
        c.search(sort_by="rank", limit=1)
    except NotImplementedError:
        return
    raise AssertionError("expected NotImplementedError for sort_by+limit")


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
