import inspect
from typing import Any, Callable, Dict


class NaiveTooler:

    tool_dict = {}

    def cust_tool(self):
        def generate_tool_schema(func: Callable) -> Dict[str, Any]:
            # Retrieve function metadata
            name = func.__name__
            description = inspect.getdoc(func)
            sig = inspect.signature(func)

            # Initialize schema dictionary
            schema = {
                "name": name,
                "description": (
                    description if description else "No description available."
                ),
                "input_schema": {"type": "object", "properties": {}, "required": []},
            }

            # Loop through parameters to build properties
            for param_name, param in sig.parameters.items():
                # Start building the property schema
                param_schema = {
                    "type": "string",  # default type if no annotation is found
                    "description": "No description available.",  # default description
                }

                # Update type based on annotation
                if param.annotation != param.empty:
                    param_schema["type"] = param.annotation

                # Check for default value
                if param.default != param.empty:
                    param_schema["default"] = param.default

                # Add to properties
                schema["input_schema"]["properties"][param_name] = param_schema

                # Add required fields
                if param.default == param.empty:
                    schema["input_schema"]["required"].append(param_name)

            self.tool_dict[name] = schema
            return func

        return generate_tool_schema
