from datetime import time

from pawpal_system import PetInfo, Task


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
