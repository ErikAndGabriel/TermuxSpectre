import importlib
import pkgutil
from pathlib import Path


def load_commands():
    commands = {}
    package_dir = Path(__file__).parent

    for info in pkgutil.iter_modules([str(package_dir)]):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"{__name__}.{info.name}")
        name = getattr(mod, "NAME", None)
        handler = getattr(mod, "run", None)
        if not name or not handler:
            continue
        if name in commands:
            continue
        commands[name] = mod
    return commands
