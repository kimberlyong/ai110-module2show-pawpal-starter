# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
The first class will be the user who can enter in their info like name, contact, and restrictions. Then they will add in a pet info class info like animal, age, special requirements, etc. From the pet, the model will determine different pet care tasks like walking, feeding times, medication, enrichment, grooming, etc. These factors will then help produce a class called daily schedule for how to take care of the dog's needs.

- What classes did you include, and what responsibilities did you assign to each?
The main classes are user, pet info, tasks, and daily plan. The user attributes are their name, contact, work schedule, and restrictions. The pet info includes basic breed, age, special requirements, and feeding requirements. The tasks class lists out how often roles like walking, feeding, medication, enrichment, and grooming occur. Finally, daily schedule organizes the information together.

**b. Design changes**

- Did your design change during implementation?
Yes.

- If yes, describe at least one change and why you made it.
One change was being more specific in the requirements. For example, for owner information, instead of just having any restrictions, there were new methods for available times and time windows. This helped make scheduling more cohesive with the tasks

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
The current scheduler takes in the Owner's schedule like time slots they have open. It also takes into account the Pet's specific needs like dietary requirements, time required to complete a task, and the pet preferences.

- How did you decide which constraints mattered most?
The current scheduler decides based on chronological order and what best fits into the owner's schedule. Having it organized chronologically makes the most sense for someone who uses it and for someone who actually needs to use it and see it working in their own schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It priortizes the human schedule even if it means pushing back a walk to an hour or two later.

- Why is that tradeoff reasonable for this scenario?
The main reason why this app was made was because the owner was having difficulty remembering everything in a busy schedule. By focusing on fitting thing into their schedule based on how long the task takes, it makes it more likely that they would actually be able to accomplish these tasks. Still, other tasks can be prioritized within those time slots like medication or feeding times over walk times.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
I used AI to help with brainstorming the flow of logic, editting the flow after visualizing it the first time, and adding in test cases to ensure that a schedule with multiple pets was working.

- What kinds of prompts or questions were most helpful?
Prompts that were very specific and guided the AI to a specific file were the most helpful because it also reduced how much it changed other files. Questions that asked to number changes or clearly walk through steps were also helpful in allowing me to understand what the computer was implementing and reference certain numbered steps that I wanted changed or I wanted explained further.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
When I asked it to suggest different ways to optimize the flowchart for scheduling, it offered about different solutions. I asked it to explain each step a little more in depth before allowing it to implement one by one.

- How did you evaluate or verify what the AI suggested?
I first made sure that it explained the change to me so I could understand what the problem was and if it needed to be fixed at all. If the change was reasonable (like a concern that there may be multiple pets) in a real-world scenario, I went ahead to allow the AI to continue.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
The tests check what would happen if there was scheduling conflicts just with different priority levels. IT also tested to see if the weekly occurrence would come back even after one was checked off for the week. Finally, another case it tested was filtering to make sure that the two filters that you could apply (which pet and completion) matched what the user had input.


- Why were these tests important?
The first test was important to ensuring that time was best spent on more important/urgent tasks like giving medication or having consistent meals. The second edge case made sure the weekly and monthly feature worked and it wasn't the same thing as a daily task. Finally, the last main case ensured that it was easy for the user to use and manage their schedule even with different viewing options.


**b. Confidence**

- How confident are you that your scheduler works correctly?
I am 4/5 confident that this will work smoothly.


- What edge cases would you test next if you had more time?
While there were quite a few test cases, there is almost always something else that can come up later like if there is a new task that doesn't have a priority assignment. Or if there is a super long task and the schedule has no where to put it that fit into the owner's schedule so it may require moving around the owner's schedule as well.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I am satisfied with the UML diagram since it was helpful to visualize the flow of information being added before actually implementing it. It also made it a lot easier to change and recognize gaps in information.


**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would redesign the schedule to be more visual. While a list format is great and works well, when a user is trying to see their schedule for the week or a month and plan out their own schedule around important pet events.


**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

There are a lot of test/edge cases to consider so while using it is great, it is also helpful to ask AI to write pytests or just consider different angles so that random cases will be captured before they occur.
