from datetime import date, time, timedelta

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


def test_scheduler_places_unscheduled_tasks_last() -> None:
    pet = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4)
    timed_task = Task("Breakfast", time(8, 0), "daily", category="meal")
    unscheduled_task = Task("Play", None, "as needed")
    pet.tasks.extend([unscheduled_task, timed_task])
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com", pets=[pet])

    schedule = Scheduler().organize_tasks(owner)

    assert schedule == [timed_task, unscheduled_task]


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
