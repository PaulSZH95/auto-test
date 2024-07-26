import ast
import os


class AstVanillaParse:

    @classmethod
    def format_docstring(cls, doc):
        """Format the extracted docstring to be more readable."""
        if doc:
            return " ".join(doc.strip().split())
        return None

    @classmethod
    def get_function_parameters(cls, func_node):
        """Extract parameters and their types from a function node."""
        params = {}
        for arg in func_node.args.args:
            # Check for type annotations
            param_name = arg.arg
            type_annotation = arg.annotation
            if type_annotation:
                # Convert the AST node for the type hint to a string
                type_name = ast.unparse(type_annotation)
            else:
                type_name = "Any"  # Use 'Any' if no type is specified
            params[param_name] = type_name
        return params

    @classmethod
    def parse_python_file(cls, file_path):
        with open(file_path, "r") as file:
            tree = ast.parse(file.read())
        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_doc = cls.format_docstring(ast.get_docstring(node))
                methods = {}
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        method_doc = cls.format_docstring(ast.get_docstring(n))
                        parameters = cls.get_function_parameters(n)
                        methods[n.name] = {
                            "docstring": method_doc,
                            "parameters": parameters,
                        }
                classes[node.name] = {"docstring": class_doc, "methods": methods}
        return classes

    @classmethod
    def parse_printable_python_file(cls, file_path):
        with open(file_path, "r") as file:
            tree = ast.parse(file.read())
        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Extracting docstring for the class
                class_doc = ast.get_docstring(node)
                methods = {}
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        # Extracting docstring for each method
                        method_doc = ast.get_docstring(n)
                        methods[n.name] = method_doc
                classes[node.name] = (class_doc, methods)
        return classes

    @classmethod
    def build_tree(cls, directory):
        tree_dict = {}
        entries = os.listdir(directory)
        entries = list(filter(lambda x: x != "console_src", entries))
        entries = [e for e in entries if not e.startswith(".")]  # Ignore hidden files
        entries.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x))
        for entry in entries:
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                tree_dict[entry] = cls.build_tree(path)
            elif entry.endswith(".py"):
                tree_dict[entry] = cls.parse_python_file(path)
        return tree_dict

    @classmethod
    def print_tree(cls, directory, prefix=""):
        entries = os.listdir(directory)
        entries = [e for e in entries if not e.startswith(".")]  # Ignore hidden files
        entries.sort(key=lambda x: (not os.path.isdir(os.path.join(directory, x)), x))
        for i, entry in enumerate(entries):
            path = os.path.join(directory, entry)
            if os.path.isdir(path):
                if i == len(entries) - 1:
                    print(f"{prefix}└── {entry}/")
                    cls.print_tree(path, prefix + "    ")
                else:
                    print(f"{prefix}├── {entry}/")
                    cls.print_tree(path, prefix + "│   ")
            elif entry.endswith(".py"):
                classes = cls.parse_printable_python_file(path)
                if i == len(entries) - 1:
                    print(f"{prefix}└── {entry}")
                else:
                    print(f"{prefix}├── {entry}")
                if classes:
                    class_prefix = prefix + (
                        "    " if i == len(entries) - 1 else "│   "
                    )
                    last_class = len(classes) - 1
                    for j, (class_name, (class_doc, methods)) in enumerate(
                        classes.items()
                    ):
                        class_doc = f" # {class_doc}" if class_doc else ""
                        if j == last_class:
                            print(f"{class_prefix}└── {class_name}{class_doc}")
                        else:
                            print(f"{class_prefix}├── {class_name}{class_doc}")
                        method_prefix = class_prefix + (
                            "    " if j == last_class else "│   "
                        )
                        last_method = len(methods) - 1
                        for k, (method, doc) in enumerate(methods.items()):
                            doc = f" # {doc}" if doc else ""
                            if k == last_method:
                                print(f"{method_prefix}└── {method}(){doc}")
                            else:
                                print(f"{method_prefix}├── {method}(){doc}")
