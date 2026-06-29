"""Behavioural tests for catalog.Catalog (current behaviour, contract 1.0).

Covers S4 limit plus regressions for query/where/sort_by/blank/unknown-field.
Run: python test_catalog.py
"""

from catalog import Catalog


def names(items):
    return [i["name"] for i in items]


def make():
    c = Catalog()
    c.add({"name": "Apple", "price": 3, "tag": "fruit"})
    c.add({"name": "banana", "price": 1, "tag": "fruit"})
    c.add({"name": "Cherry", "price": 2, "tag": "fruit"})
    c.add({"name": "date", "price": 2, "tag": "dry"})
    return c


# --- add / all / copy isolation (D1, D3) ---

def test_all_insertion_order():
    c = make()
    assert names(c.all()) == ["Apple", "banana", "Cherry", "date"]


def test_copy_on_add_isolation():
    c = Catalog()
    src = {"name": "X", "nested": {"k": 1}}
    c.add(src)
    src["name"] = "MUTATED"
    src["nested"]["k"] = 999
    assert names(c.all()) == ["X"]
    assert c.all()[0]["nested"]["k"] == 1


def test_copy_on_read_isolation():
    c = make()
    got = c.search()
    got[0]["name"] = "MUTATED"
    got[0]["price"] = -1
    assert names(c.all()) == ["Apple", "banana", "Cherry", "date"]
    assert c.all()[0]["price"] == 3


# --- search() no-arg == all() ---

def test_search_no_args_lists_all():
    c = make()
    assert names(c.search()) == names(c.all())


# --- query (D4 substring; D6 blank) ---

def test_query_case_insensitive_substring():
    c = make()
    assert names(c.search(query="a")) == ["Apple", "banana", "date"]


def test_query_keeps_insertion_order():
    c = make()
    assert names(c.search(query="A")) == ["Apple", "banana", "date"]


def test_query_no_match_empty():
    c = make()
    assert c.search(query="zzz") == []


def test_query_none_is_list_mode():
    c = make()
    assert names(c.search(query=None)) == names(c.all())


def test_blank_query_returns_empty():
    c = make()
    assert c.search(query="") == []
    assert c.search(query="   ") == []


# --- where (D5 equality, AND, missing-key ValueError) ---

def test_where_single_key():
    c = make()
    assert names(c.search(where={"tag": "fruit"})) == ["Apple", "banana", "Cherry"]


def test_where_multi_key_and():
    c = make()
    assert names(c.search(where={"tag": "fruit", "price": 2})) == ["Cherry"]


def test_where_no_match_empty():
    c = make()
    assert c.search(where={"tag": "fruit", "price": 99}) == []


def test_where_empty_dict_lists_all():
    c = make()
    assert names(c.search(where={})) == names(c.all())


def test_where_compose_with_query():
    c = make()
    assert names(c.search(query="a", where={"tag": "fruit"})) == ["Apple", "banana"]


def test_where_missing_key_raises():
    c = make()
    try:
        c.search(where={"nope": 1})
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for unknown where key")


def test_where_key_missing_on_some_item_raises():
    c = Catalog()
    c.add({"name": "a", "k": 1})
    c.add({"name": "b"})  # missing 'k'
    try:
        c.search(where={"k": 1})
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError when key missing on some item")


# --- sort_by (D7 ascending, stable, missing-key ValueError, type TypeError) ---

def test_sort_by_ascending():
    c = make()
    assert names(c.search(sort_by="price")) == ["banana", "Cherry", "date", "Apple"]


def test_sort_by_is_stable():
    c = make()
    # price==2: Cherry (idx2) before date (idx3); insertion order preserved.
    out = names(c.search(sort_by="price"))
    assert out.index("Cherry") < out.index("date")


def test_sort_after_filter():
    c = make()
    assert names(c.search(where={"tag": "fruit"}, sort_by="price")) == [
        "banana", "Cherry", "Apple"
    ]


def test_sort_missing_field_raises():
    c = Catalog()
    c.add({"name": "a", "p": 1})
    c.add({"name": "b"})  # missing 'p'
    try:
        c.search(sort_by="p")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for sort_by missing on a result")


def test_sort_incomparable_types_raises():
    c = Catalog()
    c.add({"name": "a", "v": 1})
    c.add({"name": "b", "v": "x"})
    try:
        c.search(sort_by="v")
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError for incomparable sort values")


# --- limit (D8, NEW in S4) ---

def test_limit_caps_results():
    c = make()
    assert names(c.search(limit=2)) == ["Apple", "banana"]


def test_limit_top_n_after_sort():
    c = make()
    # sorted by price asc: banana(1), Cherry(2), date(2), Apple(3); top 2.
    assert names(c.search(sort_by="price", limit=2)) == ["banana", "Cherry"]


def test_limit_with_query_and_where_and_sort():
    c = make()
    # query 'a' -> Apple, banana, date; where tag=fruit -> Apple, banana;
    # sort price -> banana(1), Apple(3); limit 1 -> banana.
    assert names(c.search(query="a", where={"tag": "fruit"}, sort_by="price", limit=1)) == [
        "banana"
    ]


def test_limit_zero_returns_empty():
    c = make()
    assert c.search(limit=0) == []


def test_limit_above_count_returns_all():
    c = make()
    assert names(c.search(limit=99)) == names(c.all())


def test_limit_equal_count_returns_all():
    c = make()
    assert names(c.search(limit=4)) == names(c.all())


def test_limit_negative_raises_valueerror():
    c = make()
    try:
        c.search(limit=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError for negative limit")


def test_limit_non_int_raises_typeerror():
    c = make()
    for bad in (1.5, "2", [1]):
        try:
            c.search(limit=bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for limit={bad!r}")


def test_limit_bool_raises_typeerror():
    c = make()
    for bad in (True, False):
        try:
            c.search(limit=bad)
        except TypeError:
            pass
        else:
            raise AssertionError(f"expected TypeError for limit={bad!r}")


def test_limit_none_is_no_cap():
    c = make()
    assert names(c.search(limit=None)) == names(c.all())


def test_limit_does_not_mutate_internal_state():
    c = make()
    c.search(sort_by="price", limit=1)
    assert names(c.all()) == ["Apple", "banana", "Cherry", "date"]


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for t in tests:
        t()
        passed += 1
    print(f"{passed} tests passed")
