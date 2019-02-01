import pathlib
import importlib

def load_commands(path: pathlib.Path = pathlib.Path(".", "command"), main_name="_cmd_main"):
    if path.is_file():
        raise ValueError("path must point to a directory")

    if path.parts[0] == '.':
        module_str = ".".join(path.parts[1:])
    else:
        module_str = ".".join(path.parts)

    commands = {}

    for child in path.iterdir():
        if child.is_file():
            command_module = importlib.import_module(child.stem, module_str)

            commands[child.stem] = getattr(command_module, command_module)
    
    return commands