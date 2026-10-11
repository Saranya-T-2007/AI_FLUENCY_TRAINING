from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class TicketState(TypedDict):          
    question: str
    desk: str
    reply: str


def classify(state: TicketState):     
    q = state["question"].lower()
    if any(w in q for w in ("fee", "refund", "scholarship")):
        return {"desk": "accounts"}
    if any(w in q for w in ("hostel", "mess", "warden")):
        return {"desk": "hostel"}
    return {"desk": "general"}


def accounts(state: TicketState):
    return {"reply": "Forwarded to the Accounts office."}


def hostel(state: TicketState):
    return {"reply": "Forwarded to the Hostel warden."}


def general(state: TicketState):
    return {"reply": "Forwarded to the general helpdesk."}


def route(state: TicketState):         
    return state["desk"]


builder = StateGraph(TicketState)
builder.add_node("classify", classify)
builder.add_node("accounts", accounts)
builder.add_node("hostel", hostel)
builder.add_node("general", general)
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route, ["accounts", "hostel", "general"])
for n in ("accounts", "hostel", "general"):
    builder.add_edge(n, END)
graph = builder.compile()

print(graph.get_graph().draw_mermaid())  

for q in ["When is the fee due?", "What are the mess timings?", "Where is the library?"]:
    result = graph.invoke({"question": q})
    print(f"{q:32} -> desk={result['desk']:9} | {result['reply']}")