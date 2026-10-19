from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time


@dataclass
class Task:
    description: str
    scheduled_time: time | None
    frequency: str
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True


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

    def retrieve_tasks(self, owner: OwnerInfo) -> list[Task]:
        """Load tasks through the owner so every pet is included."""
        self.tasks = owner.get_all_tasks()
        return list(self.tasks)

    def organize_tasks(self, owner: OwnerInfo) -> list[Task]:
        """Order all pet tasks by scheduled time, with unscheduled tasks last."""
        self.tasks = sorted(
            self.retrieve_tasks(owner),
            key=lambda task: (
                task.scheduled_time is None,
                task.scheduled_time or time.max,
            ),
        )
        return list(self.tasks)

    def mark_completed(self, task: Task) -> None:
        """Mark a task as complete if it belongs to this schedule."""
        if not any(scheduled_task is task for scheduled_task in self.tasks):
            raise ValueError("Task is not part of this schedule.")
        task.mark_complete()
