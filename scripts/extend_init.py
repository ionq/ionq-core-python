#!/usr/bin/env python3
"""Extend generated __init__.py with exports from hand-written modules."""

import ast
from pathlib import Path

MODULES = ["exceptions", "extensions", "gates", "ionq_client", "pagination", "polling", "session"]
EXTRAS = {"types": ["UNSET", "Unset"]}

init = Path("__init__.py")
source = init.read_text()

existing_all = set()
for node in ast.walk(ast.parse(source)):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__all__":
                existing_all = {elt.value for elt in node.value.elts}

all_names = set(existing_all)
imports = []
for mod in MODULES:
    mod_tree = ast.parse(Path(f"{mod}.py").read_text())
    for node in ast.walk(mod_tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    names = sorted(elt.value for elt in node.value.elts)
                    imports.append(f"from .{mod} import {', '.join(names)}")
                    all_names.update(names)
                    all_names.add(mod)

for mod, names in EXTRAS.items():
    imports.append(f"from .{mod} import {', '.join(sorted(names))}")
    all_names.update(names)

text = source.split("__all__")[0].rstrip() + "\n"
text += "\n".join(imports) + "\n"
text += "\n__all__ = (\n" + "".join(f'    "{n}",\n' for n in sorted(all_names)) + ")\n"
init.write_text(text)
