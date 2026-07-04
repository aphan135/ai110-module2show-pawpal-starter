from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import List, Literal, Optional

PriorityLevel = Literal["low", "medium", "high"]


@dataclass
class ScheduleConstraints:
    available_minutes: int = 480
    max_tasks: Optional[int] = None
    priority_order: List[PriorityLevel] = field(default_factory=lambda: ["high", "medium", "low"])
    preferred_categories: List[str] = field(default_factory=list)
    available_start: Optional[time] = None
    available_end: Optional[time] = None


@dataclass
class Task:
    title: str
    description: str = ""
    duration_minutes: int = 0
    priority: PriorityLevel = "medium"
    recurring: bool = False
    category: str = "general"
    scheduled_date: Optional[date] = None
    preferred_start_time: Optional[time] = None
    completed: bool = False
    frequency: str = "once"

    def is_high_priority(self) -> bool:
        """Return True when this task is high priority."""
        return self.priority == "high"

    def summary(self) -> str:
        """Return a short human-readable summary of the task."""
        status = "done" if self.completed else "pending"
        date_str = self.scheduled_date.isoformat() if self.scheduled_date else "unscheduled"
        return (
            f"{self.title} ({self.category}) - {self.duration_minutes} min, "
            f"priority={self.priority}, frequency={self.frequency}, date={date_str}, status={status}"
        )

    def get_next_occurrence_date(self) -> Optional[date]:
        """Return the next scheduled date for a recurring task, if supported."""
        if not self.recurring or not self.scheduled_date:
            return None

        frequency = self.frequency.lower()
        if frequency == "daily":
            return self.scheduled_date + timedelta(days=1)
        if frequency == "weekly":
            return self.scheduled_date + timedelta(weeks=1)
        return None

    def create_next_occurrence(self) -> Optional["Task"]:
        """Create the next recurring task instance for this task."""
        next_date = self.get_next_occurrence_date()
        if next_date is None:
            return None

        return Task(
            title=self.title,
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            recurring=self.recurring,
            category=self.category,
            scheduled_date=next_date,
            preferred_start_time=self.preferred_start_time,
            completed=False,
            frequency=self.frequency,
        )

    def mark_complete(self, pet: Optional["Pet"] = None) -> Optional["Task"]:
        """Mark this task as completed and create the next recurring instance if needed."""
        self.completed = True
        next_task = self.create_next_occurrence()
        if next_task is not None and pet is not None:
            pet.add_task(next_task)
        return next_task


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str = ""
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a Task from this pet's task list (by identity)."""
        self.tasks = [existing for existing in self.tasks if existing is not task]

    def get_daily_tasks(self, target_date: Optional[date] = None) -> List[Task]:
        """Return tasks scheduled for the given date (or all tasks if None)."""
        if target_date is None:
            return list(self.tasks)

        daily_tasks: List[Task] = []
        for task in self.tasks:
            if task.scheduled_date == target_date or task.recurring:
                daily_tasks.append(task)
        return daily_tasks


@dataclass
class OwnerPreferences:
    available_minutes_per_day: int = 480
    max_tasks_per_day: Optional[int] = None
    preferred_task_order: List[PriorityLevel] = field(default_factory=lambda: ["high", "medium", "low"])
    category_preferences: List[str] = field(default_factory=list)


@dataclass
class Owner:
    name: str
    contact_info: str = ""
    pets: List[Pet] = field(default_factory=list)
    preferences: OwnerPreferences = field(default_factory=OwnerPreferences)

    def add_pet(self, pet: Pet) -> None:
        """Register a Pet under this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Unregister a Pet from this owner (by identity)."""
        self.pets = [existing for existing in self.pets if existing is not pet]

    def update_preferences(self, preferences: OwnerPreferences) -> None:
        """Replace this owner's preferences with the provided settings."""
        self.preferences = preferences

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets owned by this owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_daily_tasks(self, target_date: Optional[date] = None) -> List[Task]:
        """Return daily tasks across all pets for a given date."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_daily_tasks(target_date))
        return tasks


class Scheduler:
    def __init__(self, owner: Owner, target_date: Optional[date] = None, constraints: Optional[ScheduleConstraints] = None):
        self.owner = owner
        self.target_date = target_date
        self.constraints = constraints or ScheduleConstraints()
        self.planned_tasks: List[Task] = []

    def retrieve_all_tasks(self) -> List[Task]:
        """Fetch all tasks from the owner."""
        return self.owner.get_all_tasks()

    def retrieve_daily_tasks(self) -> List[Task]:
        """Fetch tasks for the scheduler's target date from the owner."""
        return self.owner.get_daily_tasks(self.target_date)

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by completion state, priority, duration, and title."""
        priority_order = self.constraints.priority_order
        priority_rank = {priority: index for index, priority in enumerate(priority_order)}

        def sort_key(task: Task):
            return (
                task.completed,
                priority_rank.get(task.priority, len(priority_order)),
                task.duration_minutes,
                task.title,
            )

        """Return tasks sorted by completion, priority, duration, then title."""
        return sorted(tasks, key=sort_key)

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Return tasks sorted by preferred start time, completion status, and title."""
        tasks_to_sort = tasks if tasks is not None else self.retrieve_daily_tasks()

        def sort_key(task: Task):
            time_value = task.preferred_start_time or time(23, 59, 59)
            return (task.completed, time_value, task.title)

        return sorted(tasks_to_sort, key=sort_key)

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return tasks filtered by completion status and, optionally, a pet name."""
        filtered_tasks: List[Task] = []
        pet_name_filter = pet_name.lower() if pet_name else None

        for task in self.retrieve_daily_tasks():
            if completed is not None and task.completed is not completed:
                continue
            if pet_name_filter is not None:
                matching_pet = next((pet for pet in self.owner.pets if task in pet.tasks), None)
                if matching_pet is None or matching_pet.name.lower() != pet_name_filter:
                    continue
            filtered_tasks.append(task)

        return filtered_tasks

    def find_time_conflicts(self, tasks: Optional[List[Task]] = None) -> List[tuple[Task, Task]]:
        """Return pairs of pending tasks that share the same date and preferred start time."""
        tasks_to_check = tasks if tasks is not None else self.retrieve_daily_tasks()
        conflicts: List[tuple[Task, Task]] = []

        for index, first_task in enumerate(tasks_to_check):
            for second_task in tasks_to_check[index + 1 :]:
                if first_task.completed or second_task.completed:
                    continue
                if first_task.scheduled_date != second_task.scheduled_date:
                    continue
                if first_task.preferred_start_time is None or second_task.preferred_start_time is None:
                    continue

                if first_task.preferred_start_time == second_task.preferred_start_time:
                    conflicts.append((first_task, second_task))

        return conflicts

    def generate_plan(self) -> None:
        """Build a feasible daily plan given the scheduler's constraints."""
        self.planned_tasks = []
        available_minutes = self.constraints.available_minutes
        max_tasks = self.constraints.max_tasks
        sorted_tasks = self.sort_tasks(self.retrieve_daily_tasks())

        for task in sorted_tasks:
            if task.completed:
                continue
            if task.duration_minutes > available_minutes:
                continue
            if max_tasks is not None and len(self.planned_tasks) >= max_tasks:
                break
            if self.constraints.preferred_categories and task.category not in self.constraints.preferred_categories:
                continue

            self.planned_tasks.append(task)
            available_minutes -= task.duration_minutes

    def get_total_duration(self) -> int:
        """Return total minutes for all planned tasks."""
        return sum(task.duration_minutes for task in self.planned_tasks)

    def explain_plan(self) -> str:
        """Return a human-readable explanation of the generated plan."""
        if not self.planned_tasks:
            return "No tasks were scheduled for the target date."

        lines = [f"Daily plan for {self.owner.name} on {self.target_date or 'unspecified date'}:"]
        for task in self.planned_tasks:
            lines.append(f"- {task.summary()}")
        lines.append(f"Total planned duration: {self.get_total_duration()} minutes")
        return "\n".join(lines)

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Mark the provided task as complete and add the next recurring instance when relevant."""
        matching_pet = next((pet for pet in self.owner.pets if task in pet.tasks), None)
        return task.mark_complete(pet=matching_pet)

    def add_task_to_pet(self, pet: Pet, task: Task) -> None:
        """Attach a Task to the specified Pet."""
        pet.add_task(task)

    def update_constraints(self, constraints: ScheduleConstraints) -> None:
        """Update the scheduler's constraints used during planning."""
        self.constraints = constraints
