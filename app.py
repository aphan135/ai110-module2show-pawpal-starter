import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler, ScheduleConstraints

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ app. This UI now connects to the backend classes
for owners, pets, tasks, and scheduling.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", contact_info="")

owner = st.session_state.owner

st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.contact_info = st.text_input("Contact info", value=owner.contact_info)

st.divider()

st.subheader("Pets")
with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age", min_value=0, max_value=30, value=2)
    breed = st.text_input("Breed", value="")
    care_notes = st.text_area("Care notes", value="")
    add_pet_button = st.form_submit_button("Add pet")

if add_pet_button:
    new_pet = Pet(name=pet_name, species=species, age=age, breed=breed, care_notes=care_notes)
    owner.add_pet(new_pet)
    st.success(f"Added pet {pet_name}.")

if owner.pets:
    st.success("Pet roster is ready. Review the current pets below.")
    st.table(
        [{"name": pet.name, "species": pet.species, "age": pet.age, "breed": pet.breed} for pet in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Tasks")
if owner.pets:
    selected_pet = st.selectbox("Select pet", options=owner.pets, format_func=lambda p: p.name)
    with st.form("add_task_form", clear_on_submit=True):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        category = st.text_input("Category", value="exercise")
        description = st.text_area("Description", value="")
        add_task_button = st.form_submit_button("Add task")

    if add_task_button:
        task = Task(
            title=task_title,
            description=description,
            duration_minutes=int(duration),
            priority=priority,
            category=category,
            scheduled_date=date.today(),
        )
        selected_pet.add_task(task)
        st.success(f"Added task '{task_title}' to {selected_pet.name}.")

    if selected_pet.tasks:
        scheduler = Scheduler(owner=owner, target_date=date.today())
        sorted_tasks = scheduler.sort_by_time(selected_pet.tasks)
        st.success(f"Tasks for {selected_pet.name} are sorted by preferred start time.")
        st.table(
            [
                {
                    "title": task.title,
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                    "category": task.category,
                    "preferred_start": task.preferred_start_time or "unscheduled",
                }
                for task in sorted_tasks
            ]
        )
    else:
        st.info(f"No tasks for {selected_pet.name} yet.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add at least one pet before generating a schedule.")
    else:
        scheduler = Scheduler(owner=owner, target_date=date.today())
        scheduler.update_constraints(ScheduleConstraints(available_minutes=120))
        scheduler.generate_plan()

        conflicts = scheduler.find_time_conflicts()
        if conflicts:
            st.warning("Potential time conflicts detected:")
            for first_task, second_task in conflicts:
                st.write(
                    f"- {first_task.title} and {second_task.title} both start at "
                    f"{first_task.preferred_start_time}."
                )

        st.markdown("### Today's Schedule")
        st.success("Schedule generated successfully.")
        st.text(scheduler.explain_plan())
        st.markdown("### Planned Tasks by Pet")
        for pet in owner.pets:
            pet_tasks = [task for task in scheduler.planned_tasks if task in pet.tasks]
            if pet_tasks:
                st.markdown(f"**{pet.name}**")
                st.table(
                    [
                        {
                            "task": task.title,
                            "duration": task.duration_minutes,
                            "priority": task.priority,
                            "category": task.category,
                        }
                        for task in pet_tasks
                    ]
                )
            else:
                st.info(f"{pet.name} has no planned tasks.")
