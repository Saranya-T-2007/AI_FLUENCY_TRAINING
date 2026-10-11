# day6/robust_agent.py
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import client, MODEL, banner
from day6.tools_v2 import TOOLS, TOOL_FUNCTIONS, SCHEMAS
from day6.validate import validate_arguments

SYSTEM_PROMPT = (
    "You are a Smart Home Appliance Assistant. Always run control_appliance to alter states. "
    "Use calculator for any calculation step. Valid devices: living_room_light, kitchen_fridge, bedroom_ac. "
    "If no tool is needed, answer directly."
)

MAX_TOKENS = 500
REPEAT_LIMIT = 3

def handle_tool_call(call, log=True):
    name = call.function.name
    raw = call.function.arguments or "{}"

    try:
        arguments = json.loads(raw)
    except json.JSONDecodeError as error:
        return f"Argument error: invalid JSON ({error}). Send valid JSON for '{name}'."

    function = TOOL_FUNCTIONS.get(name)
    if function is None:
        return f"Unknown tool: {name}. Available tools: {', '.join(TOOL_FUNCTIONS)}."

    problem = validate_arguments(arguments, SCHEMAS[name])
    if problem:
        return f"Argument error: {problem}"

    try:
        result = str(function(**arguments))
    except Exception as error:
        result = f"Tool error in {name}: {type(error).__name__}: {error}"

    if log:
        print(f"      {name}({arguments}) -> {result[:100]}")
    return result

def agent(question, max_steps=6, verbose=True):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    seen = {}
    max_tokens = MAX_TOKENS

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS,
            temperature=0, max_tokens=max_tokens)
        choice = response.choices[0]
        message = choice.message

        if choice.finish_reason == "length":
            if max_tokens >= 2000:
                return "Stopped: the reply was still truncated at 2000 tokens."
            max_tokens *= 2
            continue

        if not message.tool_calls:
            return (message.content or "").strip()

        messages.append({
            "role": "assistant", "content": message.content or "",
            "tool_calls": [{"id": c.id, "type": "function",
                            "function": {"name": c.function.name,
                                         "arguments": c.function.arguments}}
                           for c in message.tool_calls]})

        for call in message.tool_calls:
            signature = (call.function.name, call.function.arguments)
            seen[signature] = seen.get(signature, 0) + 1
            if seen[signature] >= REPEAT_LIMIT:
                return (f"Stopped: {call.function.name} was called {REPEAT_LIMIT} times "
                        f"with the same arguments and made no progress.")

            result = handle_tool_call(call, log=verbose)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    return "Stopped: maximum steps reached without a final answer."

if __name__ == "__main__":
    banner("ROBUST AGENT")
    for question in [
        "Turn off the kitchen_fridge and dim the living_room_light to 40%.",
        "Is there a tool to update my security system pin?",
        "Write a one-line phrase checking if the appliances are active.",
    ]:
        print("\nQ:", question)
        print("A:", agent(question))
