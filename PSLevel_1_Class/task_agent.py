import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import ast
import operator

from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from lc_config import get_model, get_vectorstore  

COURSE_FEES = {"CS101": 12000, "AI202": 18000, "DS303": 15000}
store = get_vectorstore()

MAX_DISTANCE = 0.65  

@tool
def search_handbook(query: str) -> str:
    """Search the college handbook (fees, hostel, exams, library, AI training, placements) and return matching passages."""
    docs_with_scores = store.similarity_search_with_score(query, k=3)
    
    filtered_chunks = list()
    for doc, score in docs_with_scores:
        if score <= MAX_DISTANCE:
            filtered_chunks.append(f"[{doc.metadata['source']}] {doc.page_content}")
            
    if not filtered_chunks:
        return "NO_MATCH: this is not covered in the college handbook."
        
    return "\n\n".join(filtered_chunks)

@tool
def get_course_fee(course_code: str) -> str:
    """Return the fee in rupees for a course code such as CS101, AI202 or DS303."""
    fee = COURSE_FEES.get(course_code.strip().upper())
    return f"{course_code.upper()} fee is Rs. {fee}" if fee else f"Unknown course code {course_code}"

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}

@tool
def calculator(expression: str) -> str:
    """Evaluate simple arithmetic such as '18000 + 15000' or '100 * 12'."""
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in OPS:
            return OPS[type(n.op)](ev(n.left), ev(n.right))
        raise ValueError("only + - * / on numbers")
    try:
        return str(ev(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Error: {e}"

@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check if a student with this attendance percentage (0-100) may write the end-semester exam."""
    if not (0 <= attendance_percent <= 100):
        return "Error: Attendance percentage must be explicitly between 0 and 100."
        
    
    if attendance_percent >= 75:
        return "ELIGIBLE: Student may write the exam."
    elif 65 <= attendance_percent < 75:
        return "CONDONATION: Student may write the exam after paying a condonation fee of Rs. 500 per course."
   
    else:
        return "NOT ELIGIBLE: Student cannot write the exam due to attendance below 65%."


tools = [search_handbook, get_course_fee, calculator, check_exam_eligibility]
model = get_model().bind_tools(tools)


SYSTEM = ("You are the Greenfield College helpdesk. Use search_handbook for any rule or policy, "
          "get_course_fee for course fees, calculator for arithmetic, and check_exam_eligibility "
          "for attendance evaluations. Answer briefly and name the source file. "
          "CRITICAL: If a tool returns NO_MATCH or you cannot find explicit proof, say \"I don't know\".")

def agent(state: MessagesState):
    """The LLM node: read the conversation, either answer or ask for a tool."""
    reply = model.invoke([("system", SYSTEM)] + state["messages"])
    return {"messages": [reply]}


builder = StateGraph(MessagesState)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
graph = builder.compile(checkpointer=InMemorySaver())

def ask(question, thread_id):
    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 10}
    print(f"\n[{thread_id}] USER: {question}")
    for step in graph.stream({"messages": [("user", question)]}, config, stream_mode="updates"):
        for node, update in step.items():
            for msg in update["messages"]:
                if getattr(msg, "tool_calls", None):
                    for c in msg.tool_calls:
                        print(f"   {node:6} -> call {c['name']}({c['args']})")
                elif node == "tools":
                    print(f"   {node:6} -> {msg.name} returned {msg.content[:65]!r}...")
                else:
                    print(f"   {node:6} -> ANSWER: {msg.content}")

if __name__ == "__main__":
    print("--- PART B: DIRECT TOOL ISOLATED EVALUATIONS ---")
    test_values = [82, 70, 50, 120]
    for val in test_values:
        print(f"Input: {val:3}% -> Response: {check_exam_eligibility.invoke({'attendance_percent': val})}")
        
    print("\n--- PART D: RUNNING CONTINUOUS SEQUENTIAL THREAD EVALUATION ---")
    run_thread = "task-run"
    
    ask("What CGPA do I need to be eligible for placements?", run_thread)
    ask("My attendance is 70%. Can I write the exam?", run_thread)
    ask("What is the total of the CS101 fee, the AI202 fee and the maximum late fee?", run_thread)
    ask("And if I pay only 5 days late instead?", run_thread)
    ask("What is the capital of France?", run_thread)
