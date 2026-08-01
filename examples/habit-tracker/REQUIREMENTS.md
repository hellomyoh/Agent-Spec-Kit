# REQUIREMENTS.md — Project Initial Requirements

> This file is a **sample requirements document** for a THROUGHLINE demo.
> How to use: copy the kit into your project root, overwrite `THROUGHLINE/SOURCES/REQUIREMENTS.md`
> with this file, and then run the KICKOFF prompt.

---

# 1. Basic Project Information

## Project Name

Habit Tracker

## Project Purpose

Check off, one day at a time, whether the habits I committed to were actually done, and see at a
glance how many days I have kept them going. The point is not to keep records — it is to make
**a broken streak visible**.

## Target Users

One individual. Manages their own habits. No accounts, no sharing.

## Core Value

Within 3 seconds of opening the app, you know "what I have to do today, and how many days I'm on".

## Artifact Authoring Language

English

---

# 2. Project Description

A single static web page that works the moment you open `index.html` in a browser. No server, no
build step. You create a list of habits, tap today's cell to check it off, and view the last two
weeks of records as a grid. Data is stored only in the browser's localStorage.

Since this is a tool for one person, there is no login, no account, and no server sync.

---

# 3. Core Features

## Features That Must Be Included in the MVP

* Feature 1: **Add / delete a habit** — enter a name to add a habit, and delete it from the list.
* Feature 2: **Toggle today's check** — tap today's cell to switch between done and not done.
* Feature 3: **Last-14-days grid** — for each habit, show the last 14 days of completion as a single-row grid.
* Feature 4: **Streak display** — for each habit, show as a number how many consecutive days it has been kept as of today.

## Lower-Priority Features

* Feature 1: Per-habit color
* Feature 2: Weekly completion-rate summary
* Feature 3: JSON export / import

---

# 4. User Scenarios

1. Open it for the first time. There are no habits yet, so only a "Try adding a habit" hint and an input field are visible.
2. Add "Drink 2L of water". The last-14-days grid appears entirely empty.
3. Tap today's cell. The cell fills in and the streak becomes `1 day`.
4. Open it again the next day. The grid has shifted by one day, and today's cell is empty.
5. Check off three days in a row and the streak becomes `3 days`.
6. Skip a day and then check off again, and the streak restarts from `1 day`.

---

# 5. External Integration

None. The app makes no network requests.

---

# 6. Data Requirements

## Data to Be Stored

* Data name: the habit list and per-day completion records
* Key fields: habit id, name, creation date, the dates it was completed
* Storage location: browser localStorage
* Retention period: indefinitely, until the user clears it
* Whether it is sensitive information: no. No personally identifiable information is stored.

---

# 7. Screen / UX Requirements

## Main Screens

* Screen 1: a single page. The habit-add input field at the top, the habit list below it.
* One habit row = name + last-14-days grid + streak number + delete button.

## User Flow

* Main entry path: open `index.html` directly in a browser.
* Main task flow: add → check off today → look at the grid and streak
* Exception-case flow: even when there is no stored data or it is corrupted, the app must still open normally, as an empty screen.

## Design Requirements

* Design tone: [AI-delegated]
* Whether mobile is supported: required. The grid must not break at a width of 360px.
* Accessibility requirements: check cells must be reachable and togglable by keyboard, and their state must be readable by a screen reader.
* Whether multilingual support is needed: not needed. English only.

---

# 8. Technical Conditions

## Desired Tech Stack

* Frontend: plain HTML + CSS + JavaScript (ES modules). No framework.
* Backend: none
* Database: none (localStorage)
* Infra: none. It runs by opening the file.

## Constraints That Must Be Observed

* No build step. It must work by opening `index.html`, with no `npm install`.
* Do not load external CDNs, fonts, or libraries. It must work offline.
* **Write the date and streak calculation logic as pure functions, separated from the DOM.** Tests target those pure functions.
* Browser support scope: latest Chrome / Safari / Firefox

---

# 9. Authentication / Authorization

None. There is no login.

---

# 10. Cross-Cutting (Architecture) Baseline

## Common Data Model Rules

* Dates use a **local-timezone `YYYY-MM-DD` string** as the key. Do not use UTC or timestamps as keys.
* localStorage uses **exactly one key, `habit-tracker.v1`**, and the stored object carries a `schemaVersion` field.
* Completion records are stored as "the set of dates completed". Non-completion is not stored separately.

## Naming Conventions

* camelCase for JS variables and functions, kebab-case for filenames, kebab-case for CSS classes.

## State Management Contract

* State changes only ever happen one-way, in the order **`update state → save to localStorage → render the screen`**.
  Do not patch the DOM directly and let the state and the screen drift apart.

## Input Validation (common)

* A habit name is **1–30 characters** after trimming leading and trailing whitespace, and duplicate names are not allowed.

## ★ Streak Rule — Pinned

* **A single missed day resets the streak to 0. There is no grace day and no correction.**
* This is the core policy of this app. The purpose — "make a broken streak visible" — comes from here.

---

# 11. Test / QA Requirements

## Core Scenarios That Must Be Verified

* Scenario 1: check off 3 days in a row → streak = 3. Skip a day and check off → streak = 1.
* Scenario 2: after checking off today, once midnight passes, yesterday's cell stays filled and today's cell is newly empty.
* Scenario 3: when localStorage is empty or its value is corrupted (including manual tampering), the app does not crash and comes up in an empty state.

## Areas That Need Automated Testing

* Data processing: date-key generation, streak calculation, parsing and validating stored data — unit tests on pure functions.
* Screen: not a target for automated testing. Verified by manual QA.

## Areas That Need Manual QA

* Screen usability: whether the grid and buttons overlap at a width of 360px
* Exception cases: behavior when the browser has blocked localStorage (private mode, etc.)

## Features Where Regression Testing Is Important

* Feature 1: streak calculation (the first thing to break if the policy changes)
* Feature 2: date-key generation (timezone and midnight boundary)

## Quality Criteria

* Rendering 20 habits × a 14-day grid must show no perceptible lag.

---

# 12. Operations / Deployment

## Execution Environments

* Local: open `index.html` in a browser. That is all.

## Deployment Method

* Upload the static files as they are. No CI/CD, no Docker.

---

# 13. Additional Requests

* The two items below are not decided yet. Please ask about them during initialization.
  1. **The cutoff time that starts a day** — whether it should be midnight (00:00) or 4am. I tend to
     stay up late, so there are times I want to check off "today's" item just after midnight, and I
     don't know which is better.
  2. **Whether past dates can be checked off retroactively** — whether I should be able to fill in
     something I did yesterday but forgot to tap, or whether only today's cell should be tappable.
* The upper limit on the number of habits is [AI-delegated].
