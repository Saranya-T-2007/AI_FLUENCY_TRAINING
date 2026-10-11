

def validate_arguments(args: dict, schema: dict) -> str | None:
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    
    
    for field in required:
        if field not in args:
            return f"Missing required argument: '{field}'."
            
   
    for key in args:
        if key not in properties:
            return f"Unexpected argument: '{key}'. Allowed: {list(properties.keys())}."
            
        
        val = args[key]
        expected_type = properties[key]["type"]
        if expected_type == "string" and not isinstance(val, str):
            return f"Argument '{key}' must be a string, got {type(val).__name__}."
        elif expected_type == "integer" and (not isinstance(val, int) or isinstance(val, bool)):
            return f"Argument '{key}' must be an integer, got {type(val).__name__}."
            
     
        if "enum" in properties[key]:
            allowed = properties[key]["enum"]
            if val not in allowed:
                return f"Value '{val}' outside allowed enum configuration list {allowed}."
                
    return None
