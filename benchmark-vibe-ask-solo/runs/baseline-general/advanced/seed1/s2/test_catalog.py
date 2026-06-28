"""Tests for catalog.Catalog, focused on the where={k: v} equality filter.

Uses the stdlib unittest framework so it runs without third-party deps:
    python -m unittest test_catalog -v
"""

import unittest

from catalog import Catalog


def _stocked_catalog() -> Catalog:
    c = Catalog()
    c.add({"name": "Apple", "color": "red", "kind": "fruit"})
    c.add({"name": "Cherry", "color": "red", "kind": "fruit"})
    c.add({"name": "Lime", "color": "green", "kind": "fruit"})
    return c


class WhereFilterTests(unittest.TestCase):
    def test_where_single_key_match(self):
        c = _stocked_catalog()
        names = [item["name"] for item in c.search(where={"color": "red"})]
        self.assertEqual(names, ["Apple", "Cherry"])

    def test_where_no_match_returns_empty(self):
        c = _stocked_catalog()
        self.assertEqual(c.search(where={"color": "blue"}), [])

    def test_where_multiple_keys_are_anded(self):
        c = _stocked_catalog()
        names = [item["name"] for item in c.search(where={"color": "red", "kind": "fruit"})]
        self.assertEqual(names, ["Apple", "Cherry"])

        # Both keys must match; a conflicting pair yields nothing.
        self.assertEqual(c.search(where={"color": "red", "kind": "veg"}), [])

    def test_where_combines_with_query(self):
        c = _stocked_catalog()
        names = [item["name"] for item in c.search(query="c", where={"color": "red"})]
        self.assertEqual(names, ["Cherry"])

    def test_where_missing_key_raises_value_error(self):
        c = _stocked_catalog()
        with self.assertRaises(ValueError):
            c.search(where={"price": 10})

    def test_where_key_missing_from_some_items_raises_value_error(self):
        c = _stocked_catalog()
        c.add({"name": "Bread"})  # has no 'color' field
        with self.assertRaises(ValueError):
            c.search(where={"color": "red"})

    def test_where_none_applies_no_filter(self):
        c = _stocked_catalog()
        self.assertEqual(len(c.search(where=None)), 3)

    def test_where_returns_copies(self):
        c = _stocked_catalog()
        result = c.search(where={"color": "red"})
        result[0]["color"] = "mutated"
        self.assertEqual(c.search(where={"color": "red"})[0]["color"], "red")


if __name__ == "__main__":
    unittest.main()
