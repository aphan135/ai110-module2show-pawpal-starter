# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
    The system should allow a user to enter basic owner and pet information, add and manage pet care tasks, and generate a daily schedule that shows the planned tasks for the day.
    In natural language, the core user actions are: first, a user can create a pet profile and provide basic details about the owner and pet; second, the user can add care tasks such as walks, feeding, medication, or grooming, including how long each task takes and how important it is; and third, the user can generate and review a daily plan that organizes those tasks into a practical schedule for the day.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
    After reviewing the class skeleton with AI feedback, I added explicit scheduling support and stronger constraint modeling. I introduced `scheduled_date` and `preferred_start_time` on `Task`, added `ScheduleConstraints` and `OwnerPreferences` classes, and linked `Schedule` to `Owner` so decisions can respect owner preferences.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the scheduler currently checks for conflicts only when two tasks share the exact same preferred start time. It does not yet analyze full overlap across durations, such as a 30-minute walk starting at 8:00 and a 20-minute grooming task starting at 8:15. This keeps the logic lightweight and easy to understand for a small pet-care app, while still catching obvious scheduling collisions that would confuse a pet owner.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
