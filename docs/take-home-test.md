# Linq Data Candidate Take-Home Test

## 🌇 **Scenario**

You are working in an **event-driven system** where messages are emitted onto an event bus. A worker service processes these events in real time, performing key calculations. However, an issue has occurred:

- Some events were **missed** or **processed incorrectly** due to an error.
- You now need to **recalculate** the results **without relying on a traditional database** for storing historical event data.

## 💻 **Your Task**

1. **Explain your approach:**
    - How would you recover and back-calculate the missing/incorrect data?
    - What tools, strategies, or techniques would you use?
    - How would you ensure accuracy and consistency in the recalculated results?
2. **Provide a solution:**
    - Write a small script or code snippet demonstrating your approach.
    - You can use **Python, JavaScript, or any language of your choice**.
    - The solution doesn’t need to be production-ready but should demonstrate how you would solve the problem.
3. **Write-up:**
    - Summarize your approach and why you chose it.
    - Discuss any trade-offs or limitations.
    - If you had access to more tools (e.g., a database, logs, etc.), how would your approach change?
    - If applicable, discuss how your solution would scale if this system processed millions of events per hour.

## 📓 **Notes**

- You will likely need to make reasonable assumptions and state them clearly in your response.
- If you see multiple valid approaches, briefly discuss why you’d choose one over the other.

## **📌 Submission Instructions**

### **GitHub Repository**

1. Create a **GitHub repository** for your submission. (Can be public or private, if private you need to send me a invite to be a collaborator as part of the submission email)
2. Add the following files:
    - A `README.md` containing your written responses, approach, and explanations.
    - Any code files or scripts demonstrating your solution.
3. Invite pdsullivan (GitHub username) as a collaborator to the repository.
4. Email [patrick@linqapp.com](mailto:patrick@linqapp.com) with the subject line: `Data Take-Home Test Submission`
and include a link to the repository.