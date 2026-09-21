# Day 1 — Comparing a Plain Chatbot, Rule-Based Workflow, and AI Agent

## 1. Scenario

For this task, I selected a college course-fee assistant as my private-data scenario.

The private course-fee data used in this scenario is:

| Course | Fee |
|---|---:|
| CS101 | ₹12,000 |
| AI202 | ₹18,000 |
| DS303 | ₹15,000 |

The same user requests were tested using three different approaches: a plain chatbot, a rule-based workflow, and an AI agent.

The questions used for testing were:

1. What is the fee for AI202?
2. What is the total fee for CS101 and AI202 after a 10% scholarship?
3. Is DS303 more expensive than CS101, and by how much?
4. Write a two-line welcome message for new AI students.

---

## 2. Plain Chatbot

The plain chatbot mainly uses an LLM to generate responses to the user's questions. It does not use a tool to access the private course-fee data.

The user's question is directly sent to the LLM and the generated response is returned to the user. No predefined workflow rules or external tools are used.

This approach is flexible for general conversation and text generation. However, it cannot directly retrieve the private course-fee information from the program. Therefore, when a question requires accurate private data, the chatbot may not be able to reliably provide the required information unless that data is included in its context.

For this scenario, the plain chatbot demonstrates the basic use of an LLM without tool access.

---

## 3. Rule-Based Workflow

The rule-based workflow uses predefined Python rules and conditions. It does not use an LLM.

The course-fee information is stored in the program. The workflow checks the user's question, identifies course codes, and applies predefined conditions to generate the response.

For example, when a course code is detected in a fee-related question, the workflow retrieves the corresponding fee from the predefined data. For supported scholarship questions, it calculates the total and applies the 10% scholarship according to the predefined logic.

The main advantage of this approach is predictable behavior for the cases covered by its rules. However, it is less flexible because every type of request must be handled using predefined conditions.

If a user asks a new type of question that is not covered by the rules, the workflow cannot automatically decide what action should be performed.

For this scenario, the rule-based workflow demonstrates how predefined steps and conditions can solve structured problems without using an LLM.

---

## 4. AI Agent

The AI agent combines an LLM, tools, and a loop.

In this project, the agent has two tools. The `get_course_fee` tool retrieves the fee of a course, while the `calculate` tool performs mathematical calculations.

The agent first receives the user's question. The LLM determines whether a tool is required. If private course information is required, it can call the course-fee tool. If a calculation is required, it can call the calculator tool.

The result from the tool is then returned to the agent. The LLM observes the result and continues processing until it can produce the final response.

For example, when calculating the total fee of CS101 and AI202 after a 10% scholarship, the agent retrieves the fees of both courses and uses the calculator to determine the final amount.

The overall process can be represented as:

**User Question → LLM → Tool Selection → Tool Execution → Tool Result → LLM → Final Answer**

This demonstrates the concept of an AI agent as an **LLM + Tools + Loop**. The agent is more flexible than a fixed workflow because it can select tools according to the user's request and can perform multiple tool calls during a single task.

---

## 5. Comparison

| Basis for comparison | Plain chatbot | Rule-based workflow | AI agent |
|---|---|---|---|
| Flexibility | Flexible for general conversation | Limited to predefined rules | Flexible because the LLM can select tools |
| Decision-making | LLM generates a response | Uses fixed conditions | LLM decides which tools/actions are needed |
| Tool usage | No tools | No external tools | Uses course-fee and calculator tools |
| Private-data access | Cannot directly access the private course data | Can access predefined private data | Accesses private data through tools |
| Multi-step task handling | Limited | Must be explicitly programmed | Can perform multiple tool calls |
| Automation | Mainly response generation | Automates predefined tasks | Automates dynamic multi-step tasks |
| Reliability | Can be unreliable when required data is unavailable | Predictable for supported cases | Depends on the LLM and tools, while tool results provide programmatic data |
 
---

## 6. Suitability Analysis

For this course-fee scenario, the AI agent is suitable when the task requires flexible questions, private-data access, calculations, and multiple steps.

The plain chatbot is useful for general text generation and conversation, but it does not directly access the private course-fee data through a tool.

The rule-based workflow can access the private course-fee data and provides predictable results for questions covered by its predefined rules. However, it becomes less flexible when new types of questions are introduced because additional rules must be written.

The AI agent combines the flexibility of an LLM with programmatic tools. It can decide which tool is needed, use the tool, observe the result, and continue processing the task.

Therefore, for this particular scenario, the AI agent provides a flexible way to combine natural-language understanding with access to private data and calculations.

---

## 7. Conclusion

A plain chatbot is appropriate for general conversation, explanation, summarization, and text-generation tasks where external private data and tools are not required.

A rule-based workflow is appropriate when the inputs, conditions, and actions are known in advance and predictable behavior is required.

An AI agent is appropriate for tasks that require flexible decision-making, private-data access, tool usage, and multiple steps. It combines an LLM with tools and a loop so that it can select actions, observe tool results, and continue until the task is completed.

This experiment demonstrates the difference between the three approaches. A plain chatbot mainly provides responses using an LLM, a rule-based workflow follows predefined steps and conditions without an LLM, while an AI agent combines an **LLM + Tools + Loop** to select tools, observe their results, and continue taking actions until the task is completed.