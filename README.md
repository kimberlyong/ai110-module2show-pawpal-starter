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
