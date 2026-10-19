from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta
from uuid import uuid4


@dataclass
class Task:
    description: str
    scheduled_time: time | None
    frequency: str
    is_completed: bool = False
    category: str = "other"
    scheduled_date: date = field(default_factory=date.today)
    recurrence_id: str = field(default_factory=lambda: uuid4().hex, repr=False)

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def next_occurrence(self, completed_on: date | None = None) -> Task | None:
        """Build the next scheduled instance for a recurring task.

        Daily tasks recur one day after ``completed_on`` and weekly tasks
        recur seven days after it. If no completion date is supplied, today's
        date is used. The returned task copies the description, time,
        frequency, and category, starts incomplete, and retains the recurrence
        identifier used to prevent duplicate instances.

        Args:
            completed_on: Date the task was completed; defaults to today.

        Returns:
            A new task dated for the next occurrence, or ``None`` when the
            task's frequency is not daily or weekly.
        """
        recurrence_days = {"daily": 1, "weekly": 7}
        interval = recurrence_days.get(self.frequency.lower())
        if interval is None:
            return None

        occurrence_date = (completed_on or date.today()) + timedelta(days=interval)
        return Task(
            description=self.description,
            scheduled_time=self.scheduled_time,
            frequency=self.frequency,
            category=self.category,
            scheduled_date=occurrence_date,
            recurrence_id=self.recurrence_id,
        )


@dataclass
class PetInfo:
    name: str
    animal: str
    breed: str
    age: int
    special_requirements: str = ""
    feeding_requirements: str = ""
    tasks: list[Task] = field(default_factory=list)


@dataclass
class OwnerInfo:
    name: str
    contact: str
    available_times: list[str] = field(default_factory=list)
    pets: list[PetInfo] = field(default_factory=list)

    def get_all_tasks(self) -> list[Task]:
        """Return a combined list of tasks belonging to all the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Scheduler:
    tasks: list[Task] = field(default_factory=list)
    owner: OwnerInfo | None = field(default=None, repr=False)

    def retrieve_tasks(self, owner: OwnerInfo) -> list[Task]:
        """Load tasks through the owner so every pet is included."""
        self.owner = owner
        self.tasks = owner.get_all_tasks()
        return list(self.tasks)

    def organize_tasks(
        self, owner: OwnerInfo, for_date: date | None = None
    ) -> list[Task]:
        """Return the selected day's tasks in display order.

        Tasks are sorted chronologically, with medication and meal tasks ahead
        of other categories when scheduled at the same time. Tasks without a
        scheduled time appear last. The selected tasks are also stored on this
        scheduler for subsequent completion operations.

        Args:
            owner: Owner whose pets' tasks are scheduled.
            for_date: Date to include; defaults to today's date.

        Returns:
            A sorted list of tasks scheduled for the selected date.
        """
        schedule_date = for_date or date.today()
        category_priority = {"medication": 0, "meal": 0}
        self.tasks = sorted(
            (
                task
                for task in self.retrieve_tasks(owner)
                if task.scheduled_date == schedule_date
            ),
            key=lambda task: (
                task.scheduled_time is None,
                task.scheduled_time or time.max,
                category_priority.get(task.category.lower(), 1),
            ),
        )
        return list(self.tasks)

    def filter_tasks(
        self,
        tasks: list[Task],
        owner: OwnerInfo,
        pet: PetInfo | None = None,
        is_completed: bool | None = None,
    ) -> list[Task]:
        """Filter schedule tasks by pet and completion status."""
        filtered_tasks = []
        for task in tasks:
            if is_completed is not None and task.is_completed != is_completed:
                continue
            if pet is not None and not any(
                pet_task is task for pet_task in pet.tasks
            ):
                continue
            if not any(
                pet_task is task
                for owner_pet in owner.pets
                for pet_task in owner_pet.tasks
            ):
                continue
            filtered_tasks.append(task)
        return filtered_tasks

    def detect_conflicts(
        self, owner: OwnerInfo, for_date: date | None = None
    ) -> list[str]:
        """Find same-time scheduling conflicts and return warning messages.

        This lightweight check groups dated tasks by exact scheduled time and
        reports every task pair sharing a time, including conflicts involving
        the same pet. Unscheduled tasks are skipped. It only returns warnings;
        it does not modify tasks or prevent schedule generation.

        Args:
            owner: Owner whose pets' tasks should be checked.
            for_date: Date to check; defaults to today's date.

        Returns:
            Warning strings for every conflicting task pair, or an empty list
            when no conflicts are found.
        """
        schedule_date = for_date or date.today()
        tasks_by_time: dict[time, list[tuple[str, Task]]] = {}
        for pet in owner.pets:
            for task in pet.tasks:
                if (
                    task.scheduled_date == schedule_date
                    and task.scheduled_time is not None
                ):
                    tasks_by_time.setdefault(task.scheduled_time, []).append(
                        (pet.name, task)
                    )

        warnings = []
        for scheduled_time, scheduled_tasks in sorted(tasks_by_time.items()):
            if len(scheduled_tasks) < 2:
                continue

            time_label = scheduled_time.strftime("%I:%M %p").lstrip("0")
            for first_index, (first_pet, first_task) in enumerate(scheduled_tasks):
                for second_pet, second_task in scheduled_tasks[first_index + 1 :]:
                    warnings.append(
                        f"Schedule conflict at {time_label}: "
                        f"{first_pet} — {first_task.description} and "
                        f"{second_pet} — {second_task.description} "
                        "are scheduled at the same time."
                    )
        return warnings

    def mark_completed(
        self, task: Task, completed_on: date | None = None
    ) -> None:
        """Complete a task in the current schedule and recur it if applicable.

        A daily or weekly task receives a new incomplete occurrence attached
        to the same pet. An existing occurrence with the same recurrence
        identifier and date is not duplicated. Tasks outside the current
        schedule raise ``ValueError``; non-recurring frequencies only update
        completion status.

        Args:
            task: Task instance to complete; it must belong to this schedule.
            completed_on: Completion date used to calculate the next
                occurrence; defaults to today.

        Raises:
            ValueError: If the task is not in this schedule or is not assigned
                to one of the scheduler owner's pets.
        """
        if not any(scheduled_task is task for scheduled_task in self.tasks):
            raise ValueError("Task is not part of this schedule.")
        if task.is_completed:
            return

        task.mark_complete()
        next_task = task.next_occurrence(completed_on)
        if next_task is None or self.owner is None:
            return

        pet = next(
            (
                pet
                for pet in self.owner.pets
                if any(pet_task is task for pet_task in pet.tasks)
            ),
            None,
        )
        if pet is None:
            raise ValueError("Task is not assigned to one of this owner's pets.")

        if not any(
            existing.recurrence_id == next_task.recurrence_id
            and existing.scheduled_date == next_task.scheduled_date
            for existing in pet.tasks
        ):
            pet.tasks.append(next_task)
