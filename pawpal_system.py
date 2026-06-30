from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List


@dataclass
class Task:
    title: str
    description: str = ""
    duration_minutes: int = 0
    priority: str = "medium"
    recurring: bool = False
    category: str = "general"

    def is_high_priority(self) -> bool:
        pass

    def summary(self) -> str:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str = ""
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_daily_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    contact_info: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass

    def update_preferences(self, preferences: Dict[str, str]) -> None:
        pass


class Schedule:
    def __init__(self, pet: Pet, date: date):
        self.pet = pet
        self.date = date
        self.planned_tasks: List[Task] = []

    def generate_plan(self, tasks: List[Task], constraints: Dict[str, str]) -> None:
        pass

    def get_total_duration(self) -> int:
        pass

    def explain_plan(self) -> str:
        pass

    def add_task_to_plan(self, task: Task) -> None:
        pass
