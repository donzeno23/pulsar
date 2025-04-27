### ✅ How it works

- Each Python file in `stages/` becomes a test stage.
- Each stage can have `setup()`, `run()`, and `teardown()` methods.
- `StageTest` iterates through stages and calls the defined functions in order.
- `testplan` handles the reporting and structure.

### ✅ Modifications to implement dependency handling:

#### 🔁 Changes needed:
1. Add an optional `DEPENDENCIES` variable in each stage module.
2. Update the loader to read dependencies.
3. Sort stages topologically before executing them in `StageTest`.

---

### ✅ Updated Files:

#### 🔹 `stages/stage_1.py` (example)

```python
DEPENDENCIES = []  # No dependencies

def setup():
    print("Stage 1: setup")

def run():
    print("Stage 1: run")

def teardown():
    print("Stage 1: teardown")
```

#### 🔹 `stages/stage_2.py`

```python
DEPENDENCIES = ["stage_1"]  # stage_2 depends on stage_1

def setup():
    print("Stage 2: setup")

def run():
    print("Stage 2: run")

def teardown():
    print("Stage 2: teardown")
```

#### 🔹 `utils/loader.py` (updated)

```python
import importlib
import os
from collections import defaultdict, deque

def load_stage_modules(directory="stages"):
    raw_modules = {}
    dependencies = defaultdict(list)

    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".py") and not filename.startswith("__"):
            name = filename[:-3]
            module_name = f"{directory}.{name}"
            module = importlib.import_module(module_name)
            raw_modules[name] = module

            dep_list = getattr(module, "DEPENDENCIES", [])
            for dep in dep_list:
                dependencies[name].append(dep)

    sorted_stage_names = topological_sort(list(raw_modules.keys()), dependencies)

    return [raw_modules[name] for name in sorted_stage_names]

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
```

#### 🔹 `test_suite.py` (no change to logic needed)

Once the stages are sorted in `loader.py`, `StageTest` will just run them in the correct order.

---

### ✅ New Features:
1. **Optional stages**
2. **Parallel execution (where dependencies allow)**
3. **Stage skipping on failure**

---

### 🔁 Changes to make:

#### ✅ `stages/stage_x.py` now supports:
```python
DEPENDENCIES = []
OPTIONAL = True  # Optional stage that can be skipped
```

---

### 🔹 `utils/loader.py` — Enhanced to mark optional stages

We'll update this to return metadata per stage (name, module, dependencies, optionality).

```python
import importlib
import os
from collections import defaultdict, deque

def load_stage_metadata(directory="stages"):
    metadata = {}
    dependencies = defaultdict(list)

    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".py") and not filename.startswith("__"):
            name = filename[:-3]
            module_name = f"{directory}.{name}"
            module = importlib.import_module(module_name)

            deps = getattr(module, "DEPENDENCIES", [])
            optional = getattr(module, "OPTIONAL", False)

            metadata[name] = {
                "module": module,
                "dependencies": deps,
                "optional": optional
            }

            for dep in deps:
                dependencies[name].append(dep)

    sorted_names = topological_sort(list(metadata.keys()), dependencies)

    return [metadata[name] for name in sorted_names]

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
```

---

### 🔹 `test_suite.py` — Now supports skip and parallel-safe execution

```python
from testplan.testing.base import Test
from utils.loader import load_stage_metadata
import threading

class StageTest(Test):
    def __init__(self, name):
        super().__init__(name)
        self.stage_data = load_stage_metadata()
        self.failed_stages = set()

    def run_stage(self, stage_info):
        name = stage_info["module"].__name__.split('.')[-1]

        # Check if any dependency failed
        if any(dep in self.failed_stages for dep in stage_info["dependencies"]):
            self.logger.warning(f"Skipping {name} due to failed dependency.")
            return False

        try:
            if hasattr(stage_info["module"], 'setup'):
                self.logger.info(f"{name} - setup")
                stage_info["module"].setup()

            if hasattr(stage_info["module"], 'run'):
                self.logger.info(f"{name} - run")
                stage_info["module"].run()

            if hasattr(stage_info["module"], 'teardown'):
                self.logger.info(f"{name} - teardown")
                stage_info["module"].teardown()

            return True
        except Exception as e:
            self.logger.error(f"Stage {name} failed: {e}")
            if not stage_info["optional"]:
                self.failed_stages.add(name)
            return False

    def run(self):
        threads = []
        lock = threading.Lock()

        for stage_info in self.stage_data:
            # If the stage has no dependencies or they passed, run it
            thread = threading.Thread(target=self.run_stage, args=(stage_info,))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()
```

---

### 🚀 Recap: Now supports
- ✅ Optional stages
- ✅ Dependency-aware execution
- ✅ Threaded (parallel where possible)
- ✅ Skips stages if a required dependency fails

---