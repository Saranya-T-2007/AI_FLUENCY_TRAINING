
import ast
import operator


APPLIANCE_POWER = {"living_room_light": 60, "kitchen_fridge": 350, "bedroom_ac": 1200}

def control_appliance(device_id: str, action: str, brightness: int = None) -> str:
    """Adjusts the state of a smart home appliance."""
    dev = device_id.strip().lower()
    if dev not in APPLIANCE_POWER:
        return f"Unknown device: '{device_id}'. Available devices: {', '.join(APPLIANCE_POWER.keys())}"
    
    if action == "dim" and brightness is None:
        return f"Argument error: Brightness level required when action is set to 'dim'."
    
    dim_str = f" to {brightness}%" if brightness is not None else ""
    return f"Success: Device '{device_id}' turned {action}{dim_str}."

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression safely."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}. Use only numbers and + - * / ( )."

TOOL_FUNCTIONS = {"control_appliance": control_appliance, "calculator": calculator}

SCHEMAS = {
    "control_appliance": {
        "type": "object",
        "properties": {
            "device_id": {"type": "string", "description": "ID of device like living_room_light"},
            "action": {"type": "string", "enum": ["on", "off", "dim"], "description": "Action to perform"},
            "brightness": {"type": "integer", "description": "Percentage value from 0 to 100"}
        },
        "required": ["device_id", "action"],
        "additionalProperties": False
    },
    "calculator": {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Mathematical string to evaluate"}
        },
        "required": ["expression"],
        "additionalProperties": False
    }
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": name,
            "description": f"Execute safe automation operations for {name}.",
            "parameters": schema
        }
    } for name, schema in SCHEMAS.items()
]
