# rank library — Rollback: restore the 1st-revision behavior

We are rolling back the most recent revision (R2, the reverse-alphabetical tie-break). **Restore the library to EXACTLY the behavior it had after the FIRST revision (R1).**

- Remove R2's behavior completely.
- Do **not** revert all the way to the original base behavior — restore the **1st-revision** behavior specifically.
- The current code reflects R2; the 1st-revision rule is **not** written in the current code. **Consult your own records / notes / specification to recall exactly what the 1st revision specified**, and restore it faithfully (including tie-break edge cases).

Write the FULL updated `solution.py`.
