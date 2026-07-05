# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial design centered on a simple pet-care management system with an owner, pets, and tasks. I planned for an `Owner` to hold pet profiles, a `Pet` to own its care tasks, and a `Task` to represent a single care activity such as a walk or medication. I also imagined a scheduling component that would turn those tasks into a daily plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes. As the implementation progressed, I expanded the model to better match the actual scheduling behavior. I added `scheduled_date`, `preferred_start_time`, and `frequency` to `Task`, introduced `ScheduleConstraints` and `OwnerPreferences`, and shifted from a generic `Schedule` concept to a more concrete `Scheduler` class. These changes made the system more realistic because the app now needs to reason about timing, priorities, and daily planning rather than just storing tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers task duration, available minutes, priority, preferred start time, scheduled date, completion status, and optional category preferences. I prioritized time and priority first because they have the clearest impact on whether the plan is practical for a busy owner. Preferred start time was also important because it makes the output more meaningful for the user and supports the sorting behavior in the UI.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff is that the conflict logic only flags tasks that share the exact same preferred start time. It does not yet handle full overlap across time intervals, such as two tasks that partially overlap but start at different times. That is reasonable for this project because the app is meant to be lightweight and easy to explain, while still surfacing the most obvious scheduling collisions.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI for several parts of the project: brainstorming the initial object model, refining the UML diagram to match the code, generating test cases, and helping debug small issues such as imports and UI logic. The most helpful prompts were ones that asked for edge cases, test plans, and changes needed to align the design with the implementation.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One example was when AI suggested adding more complex scheduling behavior too early. I did not accept that as-is because the project scope was a small pet-care scheduler, and I wanted the implementation to stay understandable. I verified the suggestion by checking the existing code structure, comparing it to the requirements, and running the test suite to confirm that the simpler approach was still correct.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested core scheduling behaviors such as ordering tasks by preferred time, marking recurring tasks complete to create the next day's occurrence, filtering tasks by pet and completion status, and detecting duplicate preferred times. These tests were important because they cover the main user-facing features of the scheduler and prevent regressions in the planning logic.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am moderately confident that the scheduler works correctly for the current scope. The existing tests pass, and the core behaviors behave as expected. If I had more time, I would add tests for empty task lists, tasks with no preferred start time, tasks that exceed the available time budget, and cases where recurring tasks use unsupported frequencies.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am most satisfied with how the scheduler and UI now work together. The app can manage pets and tasks, sort them meaningfully, and surface scheduling conflicts in a clear way.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the conflict detection so it can handle full time overlap rather than only duplicate start times, and I would make the scheduling logic more configurable for different pet-care routines.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

A key lesson was that good system design is iterative: the first diagram is helpful, but the final implementation often reveals the real responsibilities and relationships that matter most. Working with AI was most effective when I used it to explore options and verify ideas, but I still needed to test and reason through the design myself.

---

## 6. AI Strategy Reflection

**a. Most effective assistant features**

- Which AI coding assistant features were most effective for building your scheduler?

The most effective features were the ability to generate and refine code quickly, suggest tests for edge cases, and explain how to connect the model classes to the Streamlit interface. I also found it especially helpful when the assistant could review a file and suggest changes that matched the existing structure rather than introducing unrelated abstractions.

**b. Suggestion I rejected or modified**

- Give one example of an AI suggestion you rejected or modified to keep your system design clean.

One suggestion was to add a more complex scheduling engine with many extra abstraction layers early on. I rejected that approach because it would have made the project harder to follow and less aligned with the small scope of a pet-care scheduler. Instead, I kept the design focused on a simple `Scheduler` with clear responsibilities and verified the behavior with tests.

**c. Using separate chat sessions**

- How did using separate chat sessions for different phases help you stay organized?

Using separate chats for different phases helped me keep design, implementation, testing, and documentation work distinct. I could start one conversation for planning and UML updates, another for debugging and code changes, and another for README or reflection tasks. That structure kept the context focused and made it easier to revisit earlier decisions.

**d. Lead architect lessons**

- Summarize what you learned about being the "lead architect" when collaborating with powerful AI tools.

I learned that being the lead architect means guiding the direction of the system rather than letting the AI decide the structure. The assistant can generate fast solutions, but I still need to define the goals, evaluate tradeoffs, and make sure the design remains simple, testable, and aligned with the project requirements.
