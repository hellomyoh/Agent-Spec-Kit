# S4 — Scheduling

Add scheduling of approved work.

- `schedule_task`: `approved → scheduled`, taking a `slot` (an integer time slot).
- **Only an `approved` task may be scheduled.**
- **No double-booking: two `scheduled` tasks in the same project must not occupy the same
  slot.** A conflicting schedule attempt must be refused and leave the task unscheduled.

Acceptance: an approved task can be scheduled into a free slot; scheduling a second task
into the same project+slot is refused; a non-approved task cannot be scheduled.

<!-- tags: explicit(scheduling: approved-only, no slot conflict) -->
