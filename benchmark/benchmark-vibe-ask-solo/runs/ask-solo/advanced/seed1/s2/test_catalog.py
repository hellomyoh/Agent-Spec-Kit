"""Behavioural tests for catalog.Catalog.

Run with: python -m pytest test_catalog.py   (or: python test_catalog.py)
Covers insertion order, copy isolation, query text search, and the S2 `where`
equality filter (matching, multi-key AND, and the missing-key ValueError policy),
plus the still-unspecified sort_by/limit raising NotImplementedError.
"""

import copy

from catalog import Catalog


def _stocked():
    c = Catalog()
    c.add({"name": "Apple", "color": "red", "qty": 3})
    c.add({"name": "Banana", "color": "yellow", "qty": 5})
    c.add({"name": "Cherry", "color": "red", "qty": 3})
    return c


# --- prior behaviour (preserved) ---------------------------------------------

def test_all_insertion_order():
    c = _stocked()
    assert [i["name"] for i in c.all()] == ["Apple", "Banana", "Cherry"]


def test_copy_on_read_isolation():
    c = _stocked()
    out = c.all()
    out[0]["name"] = "MUTATED"
    assert c.all()[0]["name"] == "Apple"


def test_copy_on_add_isolation():
    c = Catalog()
    src = {"name": "Apple", "tags": ["fruit"]}
    c.add(src)
    src["name"] = "MUTATED"
    src["tags"].append("MUTATED")
    stored = c.all()[0]
    assert stored["name"] == "Apple"
    assert stored["tags"] == ["fruit"]


def test_query_case_insensitive_substring_in_order():
    c = _stocked()
    names = [i["name"] for i in c.search(query="a")]
    assert names == ["Apple", "Banana"]


def test_query_blank_is_list_mode():
    c = _stocked()
    assert len(c.search(query="   ")) == 3
    assert len(c.search(query=None)) == 3


def test_sort_by_and_limit_still_not_implemented():
    c = _stocked()
    for kwargs in ({"sort_by": "name"}, {"limit": 1}):
        try:
            c.search(**kwargs)
        except NotImplementedError:
            pass
        else:
            raise AssertionError(f"expected NotImplementedError for {kwargs}")


# --- S2: where equality filter -----------------------------------------------

def test_where_single_key_match():
    c = _stocked()
    names = [i["name"] for i in c.search(where={"color": "red"})]
    assert names == ["Apple", "Cherry"]


def test_where_multi_key_is_and():
    c = _stocked()
    names = [i["name"] for i in c.search(where={"color": "red", "qty": 3})]
    assert names == ["Apple", "Cherry"]
    # tightening one value drops the non-match
    assert c.search(where={"color": "red", "qty": 5}) == []


def test_where_no_match_returns_empty():
    c = _stocked()
    assert c.search(where={"color": "blue"}) == []


def test_where_combined_with_query():
    c = _stocked()
    # query "c" -> Cherry; where red keeps it
    names = [i["name"] for i in c.search(query="c", where={"color": "red"})]
    assert names == ["Cherry"]


def test_where_missing_key_raises_valueerror():
    c = _stocked()  # no item has a 'size' field
    try:
        c.search(where={"size": "L"})
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for where key missing on items")


def test_where_key_missing_on_some_items_raises_valueerror():
    c = Catalog()
    c.add({"name": "Apple", "color": "red"})
    c.add({"name": "Banana"})  # missing 'color'
    try:
        c.search(where={"color": "red"})
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError when key missing on some items")


def test_where_result_is_copy():
    c = _stocked()
    out = c.search(where={"color": "red"})
    out[0]["name"] = "MUTATED"
    assert c.all()[0]["name"] == "Apple"


def test_where_with_sort_by_still_raises():
    c = _stocked()
    try:
        c.search(where={"color": "red"}, sort_by="name")
    except NotImplementedError:
        pass
    else:
        raise AssertionError("expected NotImplementedError for where+sort_by")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} tests passed")
