from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete():
    t = Task(title="Test Task", duration_minutes=5)
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_pet_add_task_increases_count():
    p = Pet(name="TestPet", species="Dog", age=2)
    assert len(p.tasks) == 0
    t = Task(title="Feed", duration_minutes=10)
    p.add_task(t)
    assert len(p.tasks) == 1
    assert p.tasks[0] is t


def test_scheduler_filters_tasks_by_completion_and_pet_name():
    owner = Owner(name="Test Owner")
    buddy = Pet(name="Buddy", species="Dog", age=3)
    luna = Pet(name="Luna", species="Cat", age=2)
    owner.add_pet(buddy)
    owner.add_pet(luna)

    done_task = Task(title="Feed", duration_minutes=10)
    done_task.mark_complete()
    pending_task = Task(title="Walk", duration_minutes=20)

    buddy.add_task(done_task)
    luna.add_task(pending_task)

    scheduler = Scheduler(owner=owner)

    completed_tasks = scheduler.filter_tasks(completed=True)
    assert completed_tasks == [done_task]

    buddy_tasks = scheduler.filter_tasks(pet_name="buddy")
    assert buddy_tasks == [done_task]


def test_sort_by_time_returns_tasks_in_chronological_order():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Buddy", species="Dog", age=3)
    owner.add_pet(pet)

    late_task = Task(
        title="Late walk",
        duration_minutes=20,
        scheduled_date=date(2026, 7, 3),
        preferred_start_time=time(10, 0),
    )
    early_task = Task(
        title="Early feed",
        duration_minutes=10,
        scheduled_date=date(2026, 7, 3),
        preferred_start_time=time(8, 0),
    )
    pet.add_task(late_task)
    pet.add_task(early_task)

    scheduler = Scheduler(owner=owner, target_date=date(2026, 7, 3))
    ordered_tasks = scheduler.sort_by_time()

    assert ordered_tasks == [early_task, late_task]


def test_recurring_task_completion_creates_next_occurrence():
    owner = Owner(name="Test Owner")
    pet = Pet(name="Buddy", species="Dog", age=3)
    owner.add_pet(pet)

    initial_date = date(2026, 7, 3)
    task = Task(
        title="Walk",
        duration_minutes=20,
        recurring=True,
        frequency="daily",
        scheduled_date=initial_date,
    )
    pet.add_task(task)

    scheduler = Scheduler(owner=owner, target_date=initial_date)
    scheduler.mark_task_complete(task)

    assert task.completed is True
    assert len(pet.tasks) == 2
    next_task = pet.tasks[-1]
    assert next_task is not task
    assert next_task.scheduled_date == initial_date + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.frequency == "daily"


def test_scheduler_detects_time_conflicts():
    owner = Owner(name="Test Owner")
    buddy = Pet(name="Buddy", species="Dog", age=3)
    luna = Pet(name="Luna", species="Cat", age=2)
    owner.add_pet(buddy)
    owner.add_pet(luna)

    first_task = Task(title="Walk", duration_minutes=20, scheduled_date=date(2026, 7, 3), preferred_start_time=time(8, 0))
    second_task = Task(title="Feed", duration_minutes=10, scheduled_date=date(2026, 7, 3), preferred_start_time=time(8, 0))
    buddy.add_task(first_task)
    luna.add_task(second_task)

    scheduler = Scheduler(owner=owner, target_date=date(2026, 7, 3))
    conflicts = scheduler.find_time_conflicts()

    assert conflicts == [(first_task, second_task)]
