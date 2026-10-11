# day6/inject_faults.py
import json
from day6.robust_agent import handle_tool_call

class FakeFunction:
    def __init__(self, name, arguments): self.name, self.arguments = name, arguments

class FakeCall:
    def __init__(self, name, arguments, call_id="call_test"):
        self.id, self.type = call_id, "function"
        self.function = FakeFunction(name, arguments)

FAULTS = [
    ("a good call",            FakeCall("control_appliance", '{"device_id": "living_room_light", "action": "on"}')),
    ("invalid JSON",           FakeCall("control_appliance", '{"device_id": "living_room_light", "action": "on"')),
    ("unknown tool",           FakeCall("activate_alarm",    '{"status": "armed"}')),
    ("missing required",       FakeCall("control_appliance", '{}')),
    ("wrong type",             FakeCall("control_appliance", '{"device_id": 101, "action": "on"}')),
    ("value outside the enum", FakeCall("control_appliance", '{"device_id": "living_room_light", "action": "explode"}')),
    ("invented extra argument",FakeCall("control_appliance", '{"device_id": "living_room_light", "action": "on", "timer": 30}')),
    ("unknown device id",      FakeCall("control_appliance", '{"device_id": "garage_door", "action": "off"}')),
    ("unsafe expression",      FakeCall("calculator",        json.dumps({"expression": "__import__('os').system('ls')"}))),
    ("empty arguments string", FakeCall("calculator",        '')),
]

if __name__ == "__main__":
    print("=" * 78)
    for label, call in FAULTS:
        result = handle_tool_call(call, log=False)
        print(f"{label:<26} -> {result[:72]}")
    print("=" * 78)
    print("Every line above is a STRING. Nothing raised, nothing crashed:")
    print("each message goes back to the model, which can try again.")
