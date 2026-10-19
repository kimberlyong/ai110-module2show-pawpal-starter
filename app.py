from datetime import time

import streamlit as st

from pawpal_system import OwnerInfo, PetInfo, Scheduler, Task


def update_task_completion(task: Task, state_key: str) -> None:
    completed = st.session_state[state_key]
    if completed:
        st.session_state.scheduler.mark_completed(task)
    else:
        task.is_completed = False


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.write("Add pets and their care tasks to build a combined daily schedule.")

if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()
if "schedule" not in st.session_state:
    st.session_state.schedule = []

owner = st.session_state.owner

if owner is None:
    st.subheader("Owner information")
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name")
        owner_contact = st.text_input("Contact information")
        owner_submitted = st.form_submit_button("Save owner")

    if owner_submitted:
        if not owner_name.strip() or not owner_contact.strip():
            st.error("Enter an owner name and contact information.")
        else:
            st.session_state.owner = OwnerInfo(
                name=owner_name.strip(),
                contact=owner_contact.strip(),
            )
            st.rerun()
else:
    st.subheader(f"Owner: {owner.name}")

    with st.expander("Add a pet"):
        with st.form("pet_form"):
            pet_name = st.text_input("Pet name")
            animal = st.selectbox("Animal", ["dog", "cat", "other"])
            breed = st.text_input("Breed")
            age = st.number_input("Age", min_value=0, max_value=100, value=1)
            pet_submitted = st.form_submit_button("Add pet")

        if pet_submitted:
            if not pet_name.strip():
                st.error("Enter a name for the pet.")
            else:
                owner.pets.append(
                    PetInfo(
                        name=pet_name.strip(),
                        animal=animal,
                        breed=breed.strip(),
                        age=int(age),
                    )
                )
                st.session_state.schedule = []
                st.success(f"Added {pet_name.strip()}.")

    st.subheader("Pets and care tasks")
    if not owner.pets:
        st.info("Add a pet before entering care tasks.")
    else:
        with st.form("task_form"):
            selected_pet_index = st.selectbox(
                "Pet",
                range(len(owner.pets)),
                format_func=lambda index: owner.pets[index].name,
            )
            description = st.text_input("Task description")
            scheduled_time = st.time_input("Task time", value=time(8, 0))
            category = st.selectbox(
                "Task type", ["other", "medication", "meal", "walk"]
            )
            frequency = st.selectbox(
                "Frequency", ["daily", "weekly", "as needed"]
            )
            task_submitted = st.form_submit_button("Add task")

        if task_submitted:
            if not description.strip():
                st.error("Enter a task description.")
            else:
                task = Task(
                    description=description.strip(),
                    scheduled_time=scheduled_time,
                    frequency=frequency,
                    category=category,
                )
                owner.pets[selected_pet_index].tasks.append(task)
                st.session_state.schedule = []
                st.success(f"Added task for {owner.pets[selected_pet_index].name}.")

        for pet in owner.pets:
            with st.expander(f"{pet.name} ({pet.animal})"):
                if pet.tasks:
                    for task in pet.tasks:
                        task_time = (
                            task.scheduled_time.strftime("%I:%M %p").lstrip("0")
                            if task.scheduled_time is not None
                            else "No time set"
                        )
                        status = "Complete" if task.is_completed else "Not complete"
                        st.write(
                            f"{task.scheduled_date.strftime('%b %d')} "
                            f"{task_time} — {task.description} "
                            f"[{task.category.title()}] "
                            f"({task.frequency}; {status})"
                        )
                else:
                    st.write("No tasks added yet.")

    st.subheader("Today's schedule")
    if st.button("Generate schedule", disabled=not owner.get_all_tasks()):
        st.session_state.schedule = st.session_state.scheduler.organize_tasks(owner)

    if st.session_state.schedule:
        for warning in st.session_state.scheduler.detect_conflicts(owner):
            st.warning(warning)

        pet_indices_by_task = {
            id(task): pet_index
            for pet_index, pet in enumerate(owner.pets)
            for task in pet.tasks
        }
        pet_options: list[int | None] = [None, *range(len(owner.pets))]
        selected_pet = st.selectbox(
            "Filter by pet",
            pet_options,
            format_func=lambda index: (
                "All pets" if index is None else owner.pets[index].name
            ),
        )
        selected_status = st.selectbox(
            "Filter by task status",
            ["All tasks", "Not complete", "Complete"],
        )
        visible_tasks = [
            task
            for task in st.session_state.schedule
            if (
                selected_pet is None
                or pet_indices_by_task[id(task)] == selected_pet
            )
            and (
                selected_status == "All tasks"
                or task.is_completed == (selected_status == "Complete")
            )
        ]
        if not visible_tasks:
            st.info("No tasks match these filters.")

        for task in visible_tasks:
            pet_name = owner.pets[pet_indices_by_task[id(task)]].name
            task_time = (
                task.scheduled_time.strftime("%I:%M %p").lstrip("0")
                if task.scheduled_time is not None
                else "No time set"
            )
            st.write(
                f"{task_time} — {pet_name}: {task.description} "
                f"({task.category.title()}; {task.frequency})"
            )
            completion_key = f"task_completed_{id(task)}"
            st.checkbox(
                "Complete",
                value=task.is_completed,
                key=completion_key,
                on_change=update_task_completion,
                args=(task, completion_key),
            )
