# CONVERSATION — S5

## Request (user, this session)

> 없는 필드로 거를 때 에러 빵 터지는 거 실제로 써보니 좀 짜증나네. 바꾸자 —
> 그 필드 없으면 그냥 빈 결과 주고 안 터지게 해줘.

Translation / intent: filtering with `where` on a field that no item has currently
throws an error, which is annoying in practice. Change it so that when the field
doesn't exist, `search` just returns an empty result instead of raising.

## Plan

- This reverses the S2 policy where an unknown `where` field raised `KeyError`
  ("a typo is a mistake, not an empty result"). The user has now used it for real
  and wants the opposite: unknown field => empty result, no error.
- Remove the `known_fields` / `unknown` check and the `raise KeyError`.
- Replace the match test `it.get(field) == value` with `field in it and it[field] == value`.
  - This makes an item match only when it actually carries the field with that value.
  - A field that NO item has therefore matches nothing => `[]` (the requested behaviour).
  - It also preserves the existing rule that a field present on only some items is
    fine (items lacking it just don't match), and avoids a subtle trap where
    `where={'field': None}` would otherwise spuriously match items that lack the
    field (`None == None`).
- Everything else (`query` substring + blank handling, `sort_by` stability,
  `limit` rules incl. `limit < 0` => `ValueError`) is left unchanged.

## Test run

`python -c "import catalog"` => IMPORT OK.

Behaviour checks (3 items: Apple/Banana fruit, Carrot veg; plus a no-category Steak):

```
unknown field        -> [] (no error)            PASS  <-- the fix
known+unknown         -> [] (no error)            PASS
where category=fruit  -> ['Apple', 'Banana']      (preserved)
where price=2         -> ['Carrot']               (preserved)
where category=veg    -> ['Carrot']               (preserved; Steak lacks category)
query 'ap'            -> ['Apple']                 (preserved)
query '  '            -> []                        (preserved)
query None list mode  -> lists all                 (preserved)
sort_by name          -> Apple,Banana,Carrot,Steak (preserved)
limit 2               -> ['Apple', 'Banana']       (preserved)
limit 0               -> []                        (preserved)
limit -1              -> ValueError                (preserved)
where category=None   -> [] (item lacking field does not match None)  (edge handled)
```

## Summary

`search(where=...)` no longer raises when filtering on a field that no item has;
it returns an empty list, because no item can match a field it doesn't carry. The
old unknown-field `KeyError` guard was removed and the match test tightened to
`field in it and it[field] == value`. All other search behaviour is unchanged.
