from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler, ScheduleConstraints


def run_demo():
    owner = Owner(name="Aaron", contact_info="aaron.phan@example.com")

    # Create pets
    buddy = Pet(name="Buddy", species="Dog", age=3, breed="Golden Retriever", care_notes="Energetic")
    luna = Pet(name="Luna", species="Cat", age=2, breed="Siamese", care_notes="Needs evening meds")
    owner.add_pet(buddy)
    owner.add_pet(luna)

    # Sample tasks (at least three)
    today = date.today()
    walk = Task(title="Morning Walk", description="30-minute walk", duration_minutes=30, priority="high", category="exercise", scheduled_date=today)
    feed = Task(title="Feed Breakfast", description="Dry kibble", duration_minutes=10, priority="high", category="feeding", scheduled_date=today)
    meds = Task(title="Give Medicine", description="Mix into wet food", duration_minutes=5, priority="high", category="medical", scheduled_date=today)

    buddy.add_task(walk)
    buddy.add_task(feed)
    luna.add_task(meds)

    # Create scheduler and set per-owner constraints (e.g., 60 available minutes)
    scheduler = Scheduler(owner=owner, target_date=today)
    scheduler.update_constraints(ScheduleConstraints(available_minutes=60))

    # Generate plan
    scheduler.generate_plan()

    # Print today's schedule
    print("--- TODAY'S SCHEDULE ---")
    print(scheduler.explain_plan())
    print("\nPer-pet breakdown:")
    for pet in owner.pets:
        pet_tasks = [t for t in scheduler.planned_tasks if t in pet.tasks]
        print(f"\n{pet.name} ({pet.species}) - {len(pet_tasks)} tasks")
        for t in pet_tasks:
            print(f" - {t.summary()}")


if __name__ == "__main__":
    run_demo()
