from datetime import time

from pawpal_system import OwnerInfo, PetInfo, Scheduler, Task


def main() -> None:
    owner = OwnerInfo(name="Jordan", contact="jordan@example.com")

    mochi = PetInfo(name="Mochi", animal="dog", breed="Shiba Inu", age=4)
    luna = PetInfo(name="Luna", animal="cat", breed="Tabby", age=6)
    max_pet = PetInfo(name="Max", animal="dog", breed="Beagle", age=3)

    mochi.tasks.extend(
        [
            Task("Morning walk", time(8, 0), "daily"),
            Task("Breakfast", time(7, 30), "daily"),
        ]
    )
    luna.tasks.extend(
        [
            Task("Breakfast", time(7, 0), "daily"),
            Task("Give medication", time(8, 0), "daily"),
        ]
    )
    max_pet.tasks.extend(
        [
            Task("Afternoon walk", time(15, 0), "daily"),
            Task("Dinner", time(18, 0), "daily"),
        ]
    )
    owner.pets.extend([mochi, luna, max_pet])

    scheduler = Scheduler()
    todays_tasks = scheduler.organize_tasks(owner)
    conflict_warnings = scheduler.detect_conflicts(owner)
    pet_names_by_task = {
        id(task): pet.name for pet in owner.pets for task in pet.tasks
    }

    print("Today's schedule")
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"WARNING: {warning}")
    else:
        print("No scheduling conflicts found.")

    for task in todays_tasks:
        time_label = (
            task.scheduled_time.strftime("%I:%M %p").lstrip("0")
            if task.scheduled_time is not None
            else "No time set"
        )
        pet_name = pet_names_by_task[id(task)]
        print(
            f"{time_label} - {pet_name}: {task.description} "
            f"({task.frequency}; {task.priority} priority)"
        )


if __name__ == "__main__":
    main()
