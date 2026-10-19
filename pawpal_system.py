from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OwnerInfo:
    name: str
    contact: str
    work_schedule: str
    restrictions: str
    pets: list[PetInfo] = field(default_factory=list)


@dataclass
class PetInfo:
    animal: str
    breed: str
    age: int
    special_requirements: str
    feeding_requirements: str
    tasks: list[Task] = field(default_factory=list)


@dataclass
class Task:
    task_type: str
    frequency: str


@dataclass
class DailyPlan:
    tasks: list[Task] = field(default_factory=list)

    def organize_tasks(self) -> None:
        """Organize the tasks into a daily plan."""
        pass
