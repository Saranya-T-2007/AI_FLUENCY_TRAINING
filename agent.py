from config import client, MODEL
from tools import get_course_fee, calculate

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee of a course",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


questions = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]


for question in questions:

    print("\n" + "=" * 60)
    print("QUESTION:", question)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful college course assistant. Use tools when necessary."
        },
        {
            "role": "user",
            "content": question
        }
    ]

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            print("ANSWER:", message.content)
            break

        messages.append(message)

        for tool_call in message.tool_calls:

            name = tool_call.function.name
            arguments = eval(tool_call.function.arguments)

            print("TOOL:", name)

            if name == "get_course_fee":
                result = get_course_fee(arguments["course_code"])

            elif name == "calculate":
                result = calculate(arguments["expression"])

            else:
                result = "Unknown tool"

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })