import importlib
import os

from collections import defaultdict, deque
from pathlib import Path
from rich import print as rprint


def topological_sort(nodes, edges):
    in_degree = {node: 0 for node in nodes}
    for node in nodes:
        for dep in edges[node]:
            in_degree[node] += 1

    queue = deque([node for node in nodes if in_degree[node] == 0])
    sorted_list = []

    while queue:
        node = queue.popleft()
        sorted_list.append(node)
        for neighbor in nodes:
            if node in edges[neighbor]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

    if len(sorted_list) != len(nodes):
        raise ValueError("Cyclic dependency detected among stages.")

    return sorted_list


def load_stage_modules(directory: str="pulsar/stages") -> list:
    """
    Load all stage modules from the specified directory.

    Args:
        directory (str): The directory containing the stage modules to load.
            Defaults to "stages".
            Can be an absolute or relative path.
    Raises:
        ValueError: If the provided path is not a valid directory or package.
        ImportError: If a module cannot be imported.
    Example:
        >>> from pulsar.utils.loader import load_stage_modules
        >>> stage_modules = load_stage_modules("stages")
        >>> print(stage_modules)
        [<module 'pulsar.stages.get_logs' from 'pulsar/stages/get_logs.py'>]

    Returns:
        list: A list of loaded stage module objects.
    """

    raw_modules = {}
    dependencies = defaultdict(list)

    # Convert to absolute path
    directory_path = Path(directory).resolve()

    # Ensure the directory is a valid path
    if not directory_path.is_dir():
        raise ValueError(f"Provided path '{directory_path}' is not a valid directory.")
    
    # Ensure the directory is a package
    if not (directory_path / "__init__.py").exists():
        raise ValueError(f"Provided path '{directory_path}' is not a package.")
    
    # Load all modules in the directory
    stage_modules = []

    excluded_files = ["__init__.py", "base_stage.py", "factory.py"]

    for file_path in sorted(directory_path.glob("*.py")):
        if file_path.name not in excluded_files and not file_path.name.startswith("__"):
            # Convert file path to module path
            # First, get relative path from cwd
            try:
                module_path = str(file_path.relative_to(Path.cwd()))
            except ValueError:
                # If file is not under cwd, use absolute path
                module_path = str(file_path)
            
            # Convert path to module notation
            module_path = module_path.replace(os.sep, ".")[:-3]  # Remove .py extension
            
            try:
                module = importlib.import_module(module_path)

                # Handle both class-based and module-level approaches
                if hasattr(module, 'stage'):
                    rprint(f"[bold green]Loading stage: '{module_path}' of type class [/bold green]")
                    raw_modules[module_path] = module.stage
                else:
                    rprint(f"[bold green]Loading module {module_path} of type module [/bold green]")
                    raw_modules[module_path] = module

                # Check for dependencies
                dep_list = getattr(module, "DEPENDENCIES", [])
                for dep in dep_list:
                    if dep not in raw_modules:
                        raise ImportError(f"Dependency {dep} not found for module {module_path}")
                    dependencies[module_path].append(dep)
                
            except ImportError as e:
                rprint(f"[bold orange3] Warning: Could not import {module_path}: {e} [/bold orange3]")

    sorted_stage_names = topological_sort(raw_modules.keys(), dependencies)
    return sorted_stage_names
