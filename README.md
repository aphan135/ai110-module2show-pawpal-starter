
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

## � Demo Walkthrough

PawPal+ combines a simple Streamlit interface with a scheduler backend that can sort, filter, and warn about conflicts.

### Main UI features
- Add and manage owner and pet profiles.
- Add care tasks with a title, duration, priority, category, and description.
- View tasks for a selected pet in chronological order using the scheduler's sorting logic.
- Generate a daily plan and review the tasks that were included.
- See scheduler warnings when two tasks share the same preferred start time.

### Example workflow
1. Open the app and enter owner details.
2. Add a pet such as Buddy or Luna.
3. Add tasks like a walk, feeding, or medication.
4. Click Generate schedule to build today's plan.
5. Review the sorted task list and any conflict warnings before using the plan.

### Key Scheduler behaviors shown
- Sorting by time: tasks are ordered by preferred start time.
- Conflict warnings: duplicate start times are flagged for review.
- Daily planning: the scheduler builds a feasible plan within the configured time budget.
- Filtering: pending tasks can be shown for a specific pet.

### Sample CLI output
```text
--- TODAY'S SCHEDULE ---
Daily plan for Aaron on 2026-07-04:
- Give Medicine (medical) - 5 min, priority=high, frequency=once, date=2026-07-04, status=pending
- Feed Breakfast (feeding) - 10 min, priority=high, frequency=once, date=2026-07-04, status=pending
- Morning Walk (exercise) - 30 min, priority=high, frequency=once, date=2026-07-04, status=pending
- Grooming (grooming) - 15 min, priority=medium, frequency=once, date=2026-07-04, status=pending
Total planned duration: 60 minutes

Tasks sorted by preferred time:
 - Grooming at 08:00:00
 - Morning Walk at 08:00:00
 - Feed Breakfast at 12:30:00
 - Give Medicine at 20:00:00

Pending tasks for Buddy:
 - Morning Walk (exercise) - 30 min, priority=high, frequency=once, date=2026-07-04, status=pending
 - Feed Breakfast (feeding) - 10 min, priority=high, frequency=once, date=2026-07-04, status=pending
 - Grooming (grooming) - 15 min, priority=medium, frequency=once, date=2026-07-04, status=pending

Warning: time conflicts detected!
 - Morning Walk and Grooming both start at 08:00:00
```
