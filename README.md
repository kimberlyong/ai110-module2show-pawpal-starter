# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Implementation summary

The core classes are in `pawpal_system.py`. Each `Task` gets a high, medium, or low priority from its category and description. Medication and meals are high priority. Words such as "urgent" or "medicine" also make an "Other" task high priority. Enrichment and play are low priority. Other tasks default to medium. The scheduler sorts by time, then priority. Medication and meals come first when time and priority match. Tasks without a time appear last. The app shows priorities, supports filters, and warns about same-time conflicts. Completing daily or weekly tasks creates the next occurrence.

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

The sample run in the demo below shows assigned priorities and how a high-priority
medication task moves before a medium-priority walk at the same time.

## 🧪 Testing PawPal+

### Focused edge-case test plan

Use fixed dates and times in unit tests so results do not depend on when the
tests run. The highest-priority cases cover schedule ordering and recurring
task creation.

| Priority | Area | Scenario | Expected result |
|----------|------|----------|-----------------|
| P0 | Sorting | Tasks are entered out of chronological order, including morning and afternoon times. | The selected day's tasks are returned from earliest to latest. |
| P0 | Priority | A task has no priority set. | Its type and description assign high, medium, or low; an unrecognized description defaults to medium. |
| P0 | Sorting | High, medium, and low priority tasks share one time. | Tasks appear high first, then medium, then low. |
| P0 | Sorting | Medication, meal, walk, and other tasks share one time and priority. | Medication and meals appear first; tasks with equal sort keys keep their original order. |
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
collected 18 items
tests/test_pawpal.py .................. [100%]
18 passed
```


## 📐 Features

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task priority | `Task.priority`; `infer_priority()` | Assigns high, medium, or low from task type and description. |
| Sorted schedule | `Scheduler.organize_tasks()` | Sorts by time, then priority. Meals and medicine break ties. Untimed tasks come last. |
| Filters | `Scheduler.filter_tasks()` | Filter tasks by pet and completion status. |
| Conflict warnings | `Scheduler.detect_conflicts()` | Warns when tasks share a time. |
| Recurring tasks | `Task.next_occurrence()`; `Scheduler.mark_completed()` | Daily tasks repeat tomorrow. Weekly tasks repeat in seven days. Other tasks do not repeat. |

## 📸 Demo Walkthrough

1. Enter your name and contact details, then save the owner information.
2. Select **Add a pet**. Enter the pet's name, animal, breed, and age.
3. Use the task form to choose a pet, enter a task, and set its time, type, and frequency. PawPal+ assigns a priority from its type and description. "Urgent medication refill" is high, even if its type is **Other**. "Quiet enrichment" is low. An unmatched description is medium.
4. Select **Generate schedule**. PawPal+ sorts tasks by time. Tasks at the same time go high, medium, then low. Medication and meals come first when priority also matches. Untimed tasks come last.
5. Review the schedule table. It shows each task's time, pet, category, priority, frequency, and completion status. Summary counts show complete and remaining tasks.
6. Check the conflict warnings. PawPal+ warns when two or more tasks share a time, including tasks for different pets. Warnings do not hide the schedule.
7. Use the filters to show one pet or only complete or incomplete tasks. Expand **Update task completion** to mark a task done. Completing a daily or weekly task adds its next occurrence to that pet.

Running `main.py` prints a sample schedule for three pets:

```text
Today's schedule
WARNING: Schedule conflict at 8:00 AM: Mochi — Morning walk and Luna — Give medication are scheduled at the same time.
7:00 AM - Luna: Breakfast (daily; high priority)
7:30 AM - Mochi: Breakfast (daily; high priority)
8:00 AM - Luna: Give medication (daily; high priority)
8:00 AM - Mochi: Morning walk (daily; medium priority)
3:00 PM - Max: Afternoon walk (daily; medium priority)
6:00 PM - Max: Dinner (daily; high priority)
```

**Screenshot or video** *(optional)*: Add a screenshot or demo link here.
