"""Behavioural tests for catalog.Catalog (current behaviour, S6).

Run: python test_catalog.py  (exits non-zero on first failure)

Covers the full search pipeline query -> where -> sort_by -> limit and the
copy-in/copy-out invariant. The blank-query rule reflects S6/D10: a blank or
whitespace-only query is list mode (all items), superseding S3/D6's [].
"""

import copy

from catalog import Catalog


def _names(items):
    return [it["name"] for it in items]


def make_catalog(items):
    c = Catalog()
    for it in items:
        c.add(it)
    return c


# --- add / all / insertion order (D1, D3) ---------------------------------

def test_all_insertion_order():
    c = make_catalog([{"name": "b"}, {"name": "a"}, {"name": "c"}])
    assert _names(c.all()) == ["b", "a", "c"]


def test_add_copies_in():
    src = {"name": "x", "tags": ["t1"]}
    c = Catalog()
    c.add(src)
    src["name"] = "MUTATED"
    src["tags"].append("t2")
    got = c.all()
    assert got[0]["name"] == "x"
    assert got[0]["tags"] == ["t1"]


def test_all_copies_out():
    c = make_catalog([{"name": "x", "tags": ["t1"]}])
    got = c.all()
    got[0]["name"] = "MUTATED"
    got[0]["tags"].append("t2")
    again = c.all()
    assert again[0]["name"] == "x"
    assert again[0]["tags"] == ["t1"]


# --- query: None and blank -> list mode (D10 supersedes D6) ----------------

def test_query_none_is_list_mode():
    c = make_catalog([{"name": "b"}, {"name": "a"}])
    assert _names(c.search()) == ["b", "a"]
    assert _names(c.search(query=None)) == ["b", "a"]


def test_query_blank_is_list_mode():
    # S6/D10: blank/whitespace-only query now returns ALL items (was [] under D6).
    c = make_catalog([{"name": "b"}, {"name": "a"}, {"name": "c"}])
    assert _names(c.search(query="")) == ["b", "a", "c"]
    assert _names(c.search(query="   ")) == ["b", "a", "c"]
    assert _names(c.search(query="\t\n")) == ["b", "a", "c"]


def test_query_blank_on_empty_catalog():
    c = Catalog()
    assert c.search(query="") == []


def test_query_blank_composes_with_where():
    # Blank query = list mode, so where still filters the full catalog.
    c = make_catalog([
        {"name": "a", "kind": "x"},
        {"name": "b", "kind": "y"},
        {"name": "c", "kind": "x"},
    ])
    assert _names(c.search(query="  ", where={"kind": "x"})) == ["a", "c"]


def test_query_blank_composes_with_sort_and_limit():
    c = make_catalog([{"name": "b"}, {"name": "a"}, {"name": "c"}])
    assert _names(c.search(query="", sort_by="name")) == ["a", "b", "c"]
    assert _names(c.search(query="", sort_by="name", limit=2)) == ["a", "b"]


# --- query: real text -> case-insensitive substring on name (D4) -----------

def test_query_substring_case_insensitive():
    c = make_catalog([
        {"name": "Apple"}, {"name": "banana"}, {"name": "Pineapple"},
    ])
    assert _names(c.search(query="apple")) == ["Apple", "Pineapple"]
    assert _names(c.search(query="APP")) == ["Apple", "Pineapple"]


def test_query_keeps_insertion_order():
    c = make_catalog([{"name": "zebra"}, {"name": "ant"}, {"name": "azalea"}])
    assert _names(c.search(query="a")) == ["zebra", "ant", "azalea"]


def test_query_no_match_empty():
    c = make_catalog([{"name": "a"}, {"name": "b"}])
    assert c.search(query="zzz") == []


# --- where: equality / AND / empty / missing-key (D5, D9) ------------------

def test_where_single_key():
    c = make_catalog([
        {"name": "a", "kind": "x"},
        {"name": "b", "kind": "y"},
    ])
    assert _names(c.search(where={"kind": "x"})) == ["a"]


def test_where_multi_key_and():
    c = make_catalog([
        {"name": "a", "kind": "x", "size": 1},
        {"name": "b", "kind": "x", "size": 2},
        {"name": "c", "kind": "y", "size": 1},
    ])
    assert _names(c.search(where={"kind": "x", "size": 1})) == ["a"]


def test_where_empty_lists_all():
    c = make_catalog([{"name": "a"}, {"name": "b"}])
    assert _names(c.search(where={})) == ["a", "b"]


def test_where_missing_key_all_items_returns_empty():
    # D9: a key absent from every item matches nothing (no ValueError).
    c = make_catalog([{"name": "a"}, {"name": "b"}])
    assert c.search(where={"nope": 1}) == []


def test_where_missing_key_some_items_drops_only_those():
    # D9: items lacking the key are non-matches; the rest filter normally.
    c = make_catalog([
        {"name": "a", "kind": "x"},
        {"name": "b"},
        {"name": "c", "kind": "x"},
    ])
    assert _names(c.search(where={"kind": "x"})) == ["a", "c"]


def test_where_composes_with_query():
    c = make_catalog([
        {"name": "apple", "kind": "fruit"},
        {"name": "grape", "kind": "fruit"},
        {"name": "apple pie", "kind": "dessert"},
    ])
    assert _names(c.search(query="apple", where={"kind": "fruit"})) == ["apple"]


# --- sort_by: ascending stable; missing-key ValueError; type TypeError (D7) -

def test_sort_by_ascending():
    c = make_catalog([{"name": "c"}, {"name": "a"}, {"name": "b"}])
    assert _names(c.search(sort_by="name")) == ["a", "b", "c"]


def test_sort_by_is_stable():
    c = make_catalog([
        {"name": "first", "rank": 1},
        {"name": "second", "rank": 1},
        {"name": "third", "rank": 0},
    ])
    # rank 0 first; the two rank-1 items keep insertion order (stable).
    assert _names(c.search(sort_by="rank")) == ["third", "first", "second"]


def test_sort_by_after_filtering():
    c = make_catalog([
        {"name": "apple", "n": 3},
        {"name": "apricot", "n": 1},
        {"name": "berry", "n": 2},
    ])
    assert _names(c.search(query="ap", sort_by="n")) == ["apricot", "apple"]


def test_sort_by_missing_key_raises():
    c = make_catalog([{"name": "a", "n": 1}, {"name": "b"}])
    try:
        c.search(sort_by="n")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for missing sort_by key")


def test_sort_by_incomparable_types_raises():
    c = make_catalog([{"name": "a", "v": 1}, {"name": "b", "v": "x"}])
    try:
        c.search(sort_by="v")
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError for incomparable sort_by values")


# --- limit: top N last; edge cases (D8) ------------------------------------

def test_limit_caps_results():
    c = make_catalog([{"name": "a"}, {"name": "b"}, {"name": "c"}])
    assert _names(c.search(limit=2)) == ["a", "b"]


def test_limit_top_n_after_sort():
    c = make_catalog([{"name": "c"}, {"name": "a"}, {"name": "b"}])
    assert _names(c.search(sort_by="name", limit=2)) == ["a", "b"]


def test_full_pipeline_query_where_sort_limit():
    c = make_catalog([
        {"name": "apple", "kind": "fruit", "n": 3},
        {"name": "apricot", "kind": "fruit", "n": 1},
        {"name": "avocado", "kind": "veg", "n": 2},
        {"name": "apple pie", "kind": "fruit", "n": 0},
    ])
    got = c.search(query="a", where={"kind": "fruit"}, sort_by="n", limit=2)
    assert _names(got) == ["apple pie", "apricot"]


def test_limit_zero_empty():
    c = make_catalog([{"name": "a"}, {"name": "b"}])
    assert c.search(limit=0) == []


def test_limit_at_or_above_count_returns_all():
    c = make_catalog([{"name": "a"}, {"name": "b"}])
    assert _names(c.search(limit=2)) == ["a", "b"]
    assert _names(c.search(limit=5)) == ["a", "b"]


def test_limit_none_no_cap():
    c = make_catalog([{"name": "a"}, {"name": "b"}, {"name": "c"}])
    assert _names(c.search(limit=None)) == ["a", "b", "c"]


def test_limit_negative_raises():
    c = make_catalog([{"name": "a"}])
    try:
        c.search(limit=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for negative limit")


def test_limit_non_int_raises():
    c = make_catalog([{"name": "a"}])
    for bad in (1.0, "1", [1]):
        try:
            c.search(limit=bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for limit={bad!r}")


def test_limit_bool_raises():
    # bool is an int subclass; rejected so True/False is not read as 1/0.
    c = make_catalog([{"name": "a"}])
    for bad in (True, False):
        try:
            c.search(limit=bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for limit={bad!r}")


# --- copy-on-read through search; no internal mutation ---------------------

def test_search_copies_out():
    c = make_catalog([{"name": "x", "tags": ["t1"]}])
    got = c.search(query="x")
    got[0]["name"] = "MUTATED"
    got[0]["tags"].append("t2")
    again = c.search(query="x")
    assert again[0]["name"] == "x"
    assert again[0]["tags"] == ["t1"]


def test_search_does_not_mutate_internal_state():
    items = [{"name": "c"}, {"name": "a"}, {"name": "b"}]
    c = make_catalog(items)
    before = copy.deepcopy(c.all())
    c.search(query="a", sort_by="name", limit=1)
    c.search(query="")
    assert c.all() == before


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
    print(f"OK - {len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()
