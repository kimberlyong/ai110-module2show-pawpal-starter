# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Implementation summary

The core classes are in `pawpal_system.py`. `Task` stores an activity's description, scheduled time, frequency, category, completion status, and scheduled date. `PetInfo` stores a pet's details and tasks. `OwnerInfo` manages multiple pets and `get_all_tasks()` combines their tasks. `Scheduler` retrieves tasks through the owner, orders the selected day's tasks by scheduled time (unscheduled tasks go last), prioritizes medication and meals when tasks share a time, detects same-time task conflicts as warning messages, and can mark a task in its schedule as complete. Completing a daily or weekly task creates the next dated occurrence for that pet; other task frequencies do not recur automatically. The Streamlit app supports filtering a generated schedule by pet and completion status and displays conflict warnings. `main.py` demonstrates a daily schedule for three pets, including a same-time conflict warning; `tests/test_pawpal.py` checks task completion, task addition, schedule ordering, recurring occurrences, and conflict detection.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

------------------------------------------------------------------------------------
# 7:00 AM - Luna: Breakfast (daily)
# 7:30 AM - Mochi: Breakfast (daily)
# 8:00 AM - Mochi: Morning walk (daily)
# 9:00 AM - Luna: Give medication (daily)
# 3:00 PM - Max: Afternoon walk (daily)
# 6:00 PM - Max: Dinner (daily)
------------------------------------------------------------------------------------

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

### Focused edge-case test plan

Use fixed dates and times in unit tests so results do not depend on when the
tests run. The highest-priority cases cover schedule ordering and recurring
task creation.

| Priority | Area | Scenario | Expected result |
|----------|------|----------|-----------------|
| P0 | Sorting | Tasks are entered out of chronological order, including morning and afternoon times. | The selected day's tasks are returned from earliest to latest. |
| P0 | Sorting | Medication, meal, walk, and other tasks share one scheduled time. | Medication and meal tasks appear before walk/other tasks; their relative order follows their original task-list order. |
| P0 | Sorting | A timed task and one or more tasks without a scheduled time are mixed together. | Timed tasks appear first in time order; unscheduled tasks appear last. |
| P0 | Sorting | Tasks belong to multiple pets and include dates before, on, and after the requested date. | Only tasks dated for the requested day appear, sorted together across pets. |
| P0 | Recurrence | A daily task is completed with a fixed completion date. | The original is marked complete and exactly one new, incomplete occurrence is added to the same pet for the next day. |
| P0 | Recurrence | A weekly task is completed near a month or year boundary. | Exactly one incomplete occurrence is added to the same pet seven calendar days later, including the correct month/year rollover. |
| P0 | Recurrence | The same already-completed task is marked complete more than once. | No additional occurrence is created after the first completion. |
| P1 | Sorting | Several tasks share a time and category priority, or are all unscheduled. | Tasks with equivalent sort keys retain their original order. |
| P1 | Sorting | The selected day has no tasks, or the owner has no pets/tasks. | An empty schedule is returned without an error. |
| P1 | Recurrence | A task with an unsupported recurrence frequency (for example, "as needed") is completed. | The task is marked complete, but no new occurrence is created. |
| P1 | Recurrence | A recurring task's next date already exists for the same recurrence identifier. | Completion does not add a duplicate occurrence for that date. |
| P1 | Recurrence | A task not in the current schedule is passed to `mark_completed`. | A `ValueError` is raised and no task state or pet task list is changed. |
| P1 | Recurrence | A recurring occurrence is created. | Description, time, frequency, category, and recurrence identifier are preserved; the new task has the calculated date and starts incomplete. |

For each case, assert the full task identity/order or exact occurrence count,
date, completion status, and pet assignment as appropriate. Use a
`completed_on` date explicitly for recurrence tests; do not rely on the system
date. Run the focused tests first, then the full suite with `pytest`.

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
platform win32 -- Python 3.15.0, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\kimbe\Downloads\ai110-module2show-pawpal-starter-main\ai110-module2show-pawpal-starter-main
plugins: anyio-4.15.1
collected 14 items

tests\test_pawpal.py ..............                                                                                        [100%]

====================================================== 14 passed in 0.04s =======================================================


## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.organize_tasks()` | Includes tasks scheduled for the selected date, ordered chronologically. Medication and meal tasks come before walks and other categories when their scheduled times match. Tasks without a time appear last. |
| Filtering | Streamlit schedule filters in `app.py` | Users can filter the generated schedule by pet and completion status (all, complete, or not complete). The scheduler itself selects tasks by date; it does not currently filter by available time or skip tasks. |
| Conflict handling | `Scheduler.detect_conflicts()` | Checks tasks for the selected date and returns warning messages for each pair with the same scheduled time, whether they belong to one pet or multiple pets. Unscheduled tasks are ignored. Warnings are displayed without stopping schedule generation. |
| Recurring tasks | `Task.next_occurrence()`; `Scheduler.mark_completed()` | Completing a daily task creates an incomplete task for the following day; completing a weekly task creates one seven days later. The next occurrence retains the task details and recurrence identifier and is added to the same pet. Other frequencies do not recur automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
