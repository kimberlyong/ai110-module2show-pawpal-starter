from datetime import date, time, timedelta

import pytest

from pawpal_system import OwnerInfo, PetInfo, Scheduler, Task


def test_mark_complete_changes_task_status() -> None:
    task = Task("Morning walk", time(8, 0), "daily")

    task.mark_complete()

    assert task.is_completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4)
    task = Task("Breakfast", time(7, 30), "daily")
    initial_task_count = len(pet.tasks)

    pet.tasks.append(task)

    assert len(pet.tasks) == initial_task_count + 1
    assert pet.tasks[-1] is task


def test_scheduler_prioritizes_medication_and_meals_at_the_same_time() -> None:
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4)
    walk = Task("Walk", time(8, 0), "daily", category="walk")
    medication = Task("Medicine", time(8, 0), "daily", category="medication")
    meal = Task("Breakfast", time(8, 0), "daily", category="meal")
    later_meal = Task("Dinner", time(9, 0), "daily", category="meal")
    pet.tasks.extend([walk, later_meal, medication, meal])
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])

    schedule = Scheduler().organize_tasks(owner)

    assert schedule == [medication, meal, walk, later_meal]


def test_tasks_infer_priorities_from_category_and_other_descriptions() -> None:
    assert Task("Give medicine", time(8, 0), "daily").priority == "high"
    assert (
        Task("Quiet enrichment", time(8, 0), "weekly").priority == "low"
    )
    assert Task("Brush coat", time(8, 0), "weekly").priority == "medium"
    assert (
        Task("Anything", time(8, 0), "daily", category="meal").priority
        == "high"
    )


def test_scheduler_uses_priority_to_sort_tasks_at_the_same_time() -> None:
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4)
    low = Task("Optional enrichment", time(8, 0), "as needed")
    medium = Task("Brush coat", time(8, 0), "weekly")
    high = Task("Urgent medication", time(8, 0), "daily")
    pet.tasks.extend([low, medium, high])
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])

    schedule = Scheduler().organize_tasks(owner)

    assert schedule == [high, medium, low]


def test_task_rejects_priority_outside_supported_levels() -> None:
    with pytest.raises(ValueError, match="Priority must be one of"):
        Task("Walk", time(8, 0), "daily", priority="critical")


def test_scheduler_places_unscheduled_tasks_last() -> None:
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4)
    timed_task = Task("Breakfast", time(8, 0), "daily", category="meal")
    unscheduled_task = Task("Play", None, "as needed")
    pet.tasks.extend([unscheduled_task, timed_task])
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])

    schedule = Scheduler().organize_tasks(owner)

    assert schedule == [timed_task, unscheduled_task]


def test_scheduler_filters_tasks_by_pet_and_completion_status() -> None:
    mochi_task = Task("Breakfast", time(7, 0), "daily")
    completed_luna_task = Task(
        "Medicine", time(8, 0), "daily", is_completed=True
    )
    mochi = PetInfo(
        name="Mochi",
        animal="dog",
        breed="Shiba Inu",
        age=4,
        tasks=[mochi_task],
    )
    luna = PetInfo(
        name="Luna",
        animal="cat",
        breed="Tabby",
        age=6,
        tasks=[completed_luna_task],
    )
    owner = OwnerInfo(
        name="Jordan", contact="jordan@example.com", pets=[mochi, luna]
    )

    visible_tasks = Scheduler().filter_tasks(
        [mochi_task, completed_luna_task],
        owner,
        pet=mochi,
        is_completed=False,
    )

    assert visible_tasks == [mochi_task]


def test_scheduler_sorts_across_pets_and_excludes_other_dates() -> None:
    selected_date = date(2026, 10, 18)
    earlier = Task(
        "Breakfast", time(7, 0), "daily", scheduled_date=selected_date
    )
    later = Task(
        "Walk", time(8, 0), "daily", scheduled_date=selected_date
    )
    previous_day = Task(
        "Old task",
        time(6, 0),
        "daily",
        scheduled_date=selected_date - timedelta(days=1),
    )
    mochi = PetInfo(
        name="Mochi", animal="dog", breed="Shiba Inu", age=4,
        tasks=[later, previous_day],
    )
    luna = PetInfo(
        name="Luna", animal="cat", breed="Tabby", age=6, tasks=[earlier]
    )
    owner = OwnerInfo(
        name="Jordan", contact="jordan@example.com", pets=[mochi, luna]
    )

    schedule = Scheduler().organize_tasks(owner, for_date=selected_date)

    assert schedule == [earlier, later]


def test_completing_daily_task_adds_next_day_occurrence() -> None:
    today = date(2026, 10, 18)
    task = Task("Medicine", time(8, 0), "daily", category="medication")
    task.scheduled_date = today
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4, tasks=[task])
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])
    scheduler = Scheduler()
    scheduler.organize_tasks(owner, for_date=today)

    scheduler.mark_completed(task, completed_on=today)
    scheduler.mark_completed(task, completed_on=today)

    assert task.is_completed is True
    assert len(pet.tasks) == 2
    next_task = pet.tasks[1]
    assert next_task.description == task.description
    assert next_task.scheduled_time == task.scheduled_time
    assert next_task.is_completed is False
    assert next_task.scheduled_date == today + timedelta(days=1)
    assert scheduler.organize_tasks(
        owner, for_date=today + timedelta(days=1)
    ) == [next_task]


def test_completing_weekly_task_adds_occurrence_seven_days_later() -> None:
    today = date(2026, 10, 18)
    task = Task("Grooming", time(10, 0), "weekly")
    task.scheduled_date = today
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4, tasks=[task])
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])
    scheduler = Scheduler()
    scheduler.organize_tasks(owner, for_date=today)

    scheduler.mark_completed(task, completed_on=today)

    assert len(pet.tasks) == 2
    assert pet.tasks[1].scheduled_date == today + timedelta(days=7)


def test_weekly_recurrence_copies_task_details_across_year_boundary() -> None:
    completion_date = date(2026, 12, 29)
    task = Task(
        "Give medication",
        time(21, 15),
        "weekly",
        category="medication",
        scheduled_date=completion_date,
    )
    next_task = task.next_occurrence(completion_date)

    assert next_task is not None
    assert next_task.scheduled_date == date(2027, 1, 5)
    assert next_task.description == task.description
    assert next_task.scheduled_time == task.scheduled_time
    assert next_task.frequency == task.frequency
    assert next_task.category == task.category
    assert next_task.recurrence_id == task.recurrence_id
    assert next_task.priority == task.priority
    assert next_task.is_completed is False


def test_completing_as_needed_task_does_not_add_an_occurrence() -> None:
    today = date(2026, 10, 18)
    task = Task("Play", time(10, 0), "as needed")
    task.scheduled_date = today
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4, tasks=[task])
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])
    scheduler = Scheduler()
    scheduler.organize_tasks(owner, for_date=today)

    scheduler.mark_completed(task, completed_on=today)

    assert len(pet.tasks) == 1


def test_completing_recurring_task_does_not_duplicate_existing_occurrence() -> None:
    today = date(2026, 10, 18)
    task = Task(
        "Breakfast", time(7, 30), "daily", scheduled_date=today
    )
    existing_next = task.next_occurrence(today)
    assert existing_next is not None
    pet = PetInfo(
        name="Mochi",
        animal="dog",
        breed="Shiba Inu",
        age=4,
        tasks=[task, existing_next],
    )
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])
    scheduler = Scheduler()
    scheduler.organize_tasks(owner, for_date=today)

    scheduler.mark_completed(task, completed_on=today)

    assert task.is_completed is True
    assert pet.tasks == [task, existing_next]


def test_scheduler_warns_about_same_pet_tasks_at_same_time() -> None:
    today = date(2026, 10, 18)
    pet = PetInfo(
        name="Mochi",
        animal="dog",
        breed="Shiba Inu",
        age=4,
        tasks=[
            Task("Breakfast", time(8, 0), "daily", scheduled_date=today),
            Task("Medicine", time(8, 0), "daily", scheduled_date=today),
        ],
    )
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])

    warnings = Scheduler().detect_conflicts(owner, for_date=today)

    assert len(warnings) == 1
    assert "8:00 AM" in warnings[0]
    assert "Mochi — Breakfast" in warnings[0]
    assert "Mochi — Medicine" in warnings[0]


def test_scheduler_warns_about_different_pets_at_same_time() -> None:
    today = date(2026, 10, 18)
    mochi = PetInfo(
        name="Mochi",
        animal="dog",
        breed="Shiba Inu",
        age=4,
        tasks=[Task("Morning walk", time(8, 0), "daily", scheduled_date=today)],
    )
    luna = PetInfo(
        name="Luna",
        animal="cat",
        breed="Tabby",
        age=6,
        tasks=[Task("Medication", time(8, 0), "daily", scheduled_date=today)],
    )
    owner = OwnerInfo(
        name="Jordan", contact="jordan@example.com", pets=[mochi, luna]
    )

    warnings = Scheduler().detect_conflicts(owner, for_date=today)

    assert len(warnings) == 1
    assert "Mochi — Morning walk" in warnings[0]
    assert "Luna — Medication" in warnings[0]


def test_scheduler_ignores_unscheduled_tasks_and_other_dates() -> None:
    today = date(2026, 10, 18)
    pet = PetInfo(
        name="Mochi",
        animal="dog",
        breed="Shiba Inu",
        age=4,
        tasks=[
            Task("Breakfast", time(8, 0), "daily", scheduled_date=today),
            Task("Play", None, "as needed", scheduled_date=today),
            Task(
                "Dinner",
                time(8, 0),
                "daily",
                scheduled_date=today + timedelta(days=1),
            ),
        ],
    )
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])

    assert Scheduler().detect_conflicts(owner, for_date=today) == []


def test_scheduler_reports_each_pair_for_three_tasks_at_same_time() -> None:
    today = date(2026, 10, 18)
    pet = PetInfo(
        name="Mochi",
        animal="dog",
        breed="Shiba Inu",
        age=4,
        tasks=[
            Task("Breakfast", time(8, 0), "daily", scheduled_date=today),
            Task("Medicine", time(8, 0), "daily", scheduled_date=today),
            Task("Walk", time(8, 0), "daily", scheduled_date=today),
            Task("Later walk", time(8, 30), "daily", scheduled_date=today),
            Task("Unscheduled play", None, "as needed", scheduled_date=today),
        ],
    )
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])

    warnings = Scheduler().detect_conflicts(owner, for_date=today)

    assert len(warnings) == 3
    assert all("8:00 AM" in warning for warning in warnings)
    assert all("Later walk" not in warning for warning in warnings)
    assert all("Unscheduled play" not in warning for warning in warnings)
