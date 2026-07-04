from datetime import date, time
from pawpal_system import Owner, Pet, Task, Scheduler, ScheduleConstraints


def run_demo():
    owner = Owner(name="Aaron", contact_info="aaron.phan@example.com")

    buddy = Pet(name="Buddy", species="Dog", age=3, breed="Golden Retriever", care_notes="Energetic")
    luna = Pet(name="Luna", species="Cat", age=2, breed="Siamese", care_notes="Needs evening meds")
    owner.add_pet(buddy)
    owner.add_pet(luna)

    today = date.today()

    # Add tasks out of order to demonstrate sorting by time.
    walk = Task(
        title="Morning Walk",
        description="30-minute walk",
        duration_minutes=30,
        priority="high",
        category="exercise",
        scheduled_date=today,
        preferred_start_time=time(8, 0),
    )
    feed = Task(
        title="Feed Breakfast",
        description="Dry kibble",
        duration_minutes=10,
        priority="high",
        category="feeding",
        scheduled_date=today,
        preferred_start_time=time(12, 30),
    )
    meds = Task(
        title="Give Medicine",
        description="Mix into wet food",
        duration_minutes=5,
        priority="high",
        category="medical",
        scheduled_date=today,
        preferred_start_time=time(20, 0),
    )
    grooming = Task(
        title="Grooming",
        description="Brush fur",
        duration_minutes=15,
        priority="medium",
        category="grooming",
        scheduled_date=today,
        preferred_start_time=time(8, 0),
    )

    buddy.add_task(walk)
    buddy.add_task(feed)
    luna.add_task(meds)
    buddy.add_task(grooming)

    scheduler = Scheduler(owner=owner, target_date=today)
    scheduler.update_constraints(ScheduleConstraints(available_minutes=60))
    scheduler.generate_plan()

    print("--- TODAY'S SCHEDULE ---")
    print(scheduler.explain_plan())

    print("\nTasks sorted by preferred time:")
    for task in scheduler.sort_by_time():
        print(f" - {task.title} at {task.preferred_start_time}")

    print("\nPending tasks for Buddy:")
    for task in scheduler.filter_tasks(completed=False, pet_name="Buddy"):
        print(f" - {task.summary()}")

    conflicts = scheduler.find_time_conflicts()
    if conflicts:
        print("\nWarning: time conflicts detected!")
        for first_task, second_task in conflicts:
            print(f" - {first_task.title} and {second_task.title} both start at {first_task.preferred_start_time}")
    else:
        print("\nNo time conflicts detected.")

    print("\nPer-pet breakdown:")
    for pet in owner.pets:
        pet_tasks = [t for t in scheduler.planned_tasks if t in pet.tasks]
        print(f"\n{pet.name} ({pet.species}) - {len(pet_tasks)} tasks")
        for t in pet_tasks:
            print(f" - {t.summary()}")


if __name__ == "__main__":
    run_demo()
