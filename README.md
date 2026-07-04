
# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

This project is designed as a pet care app using four main classes: `Owner`, `Pet`, `Task`, and `Schedule`.

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```bash
--- TODAY'S SCHEDULE ---
Daily plan for Aaron on 2026-06-30:
- Give Medicine (medical) - 5 min, priority=high, frequency=once, date=2026-06-30, status=pending
- Feed Breakfast (feeding) - 10 min, priority=high, frequency=once, date=2026-06-30, status=pending
- Morning Walk (exercise) - 30 min, priority=high, frequency=once, date=2026-06-30, status=pending
Total planned duration: 45 minutes

Per-pet breakdown:

Buddy (Dog) - 2 tasks
 - Feed Breakfast (feeding) - 10 min, priority=high, frequency=once, date=2026-06-30, status=pending
 - Morning Walk (exercise) - 30 min, priority=high, frequency=once, date=2026-06-30, status=pending

Luna (Cat) - 1 tasks
 - Give Medicine (medical) - 5 min, priority=high, frequency=once, date=2026-06-30, status=pending
```

## 🧪 Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover the main scheduling behaviors for PawPal+, including sorting tasks into a sensible order, confirming that completing a recurring daily task creates the next day's task, and detecting duplicate preferred times that could cause scheduling conflicts.

## 📐 Smarter Scheduling

The scheduler now includes a few lightweight features that make daily pet care planning more practical.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Orders tasks by preferred start time so the plan is easier to follow in the terminal or UI. |
| Filtering behavior | `Scheduler.filter_tasks()` | Lets the app show tasks by completion status and/or by pet name. |
| Conflict detection logic | `Scheduler.find_time_conflicts()` | Flags tasks that share the same date and preferred start time so obvious scheduling conflicts are visible. |
| Recurring task logic | `Task.get_next_occurrence_date()`, `Task.create_next_occurrence()`, `Task.mark_complete()` | When a daily or weekly task is marked complete, the system creates the next occurrence automatically. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
