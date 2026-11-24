"""Select pytest files affected by a change against a Git base commit."""
import argparse
import ast
from pathlib import Path
import subprocess
import sys


def local_imports(path):
    imports = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level or not node.module:
                raise ValueError("relative import")
            imports.add(node.module)
            imports.update(f"{node.module}.{alias.name}" for alias in node.names)
    return imports


def select_tests(changed):
    sources = {str(p): f"src.{p.stem}" for p in Path("src").glob("*.py")
               if p.stem != "__init__"}
    tests = {str(p) for p in Path("tests").glob("test_*.py")}
    # Unknown, removed and shared inputs can affect collection or every test.
    if not changed or set(changed) - (sources.keys() | tests):
        return ["tests"]
    impacted = {sources[path] for path in changed if path in sources}
    dependencies = {module: local_imports(Path(path)) for path, module in sources.items()}
    while True:
        expanded = impacted | {mod for mod, deps in dependencies.items() if deps & impacted}
        if expanded == impacted:
            break
        impacted = expanded
    selected = set(changed) & tests
    if impacted:
        selected.update(path for path in tests if local_imports(Path(path)) & impacted)
    return sorted(selected) or ["tests"]


def changed_paths(base):
    if not base or not base.strip("0"):
        return []
    output = subprocess.check_output(
        ["git", "diff", "--no-renames", "--name-only", "-z", base, "HEAD", "--"]
    )
    return output.decode().rstrip("\0").split("\0") if output else []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    try:
        selection = select_tests(changed_paths(args.base))
    except (OSError, SyntaxError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Using the full suite ({error})", file=sys.stderr)
        selection = ["tests"]
    print("\n".join(selection))
