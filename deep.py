import os
import json
import ast
import argparse
import pkg_resources

def find_files(root_dir, extensions=(".py", ".ipynb")):
    """Recursively find all files with given extensions in root_dir, ignoring directories starting with a dot."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip directories starting with a dot
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]

        for file in filenames:
            if file.endswith(extensions):
                files.append(os.path.join(dirpath, file))
    return files

def safe_parse(code, file_path):
    """Safely parse code and return AST or None if parsing fails."""
    try:
        return ast.parse(code)
    except SyntaxError as e:
        print(f"⚠️ Skipping malformed code in: {file_path} (SyntaxError: {e})")
        return None

def extract_imports_from_py(file_path):
    """Extract imported libraries from a Python script."""
    print(f"📂 Processing: {file_path}")

    # Try reading the file with UTF-8, fallback to latin-1 if it fails
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except UnicodeDecodeError:
        print(f"⚠️ Encoding issue in {file_path}, trying latin-1...")
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                code = f.read()
        except UnicodeDecodeError:
            print(f"❌ Skipping {file_path} (cannot decode file)")
            return set()  # Skip file if decoding completely fails

    tree = safe_parse(code, file_path)
    if tree is None:
        return set()  # Skip file if parsing fails

    imports = {node.names[0].name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import)}
    imports |= {node.module.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}

    return imports


def extract_imports_from_ipynb(file_path):
    """Extract imported libraries from a Jupyter Notebook."""
    print(f"📓 Processing: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
    except (json.JSONDecodeError, ValueError) as e:
        print(f"⚠️ Skipping malformed or empty notebook: {file_path} (Error: {e})")
        return set()  # Skip the file if it's not a valid notebook or is empty

    # Extract code cells
    code_cells = ["".join(cell["source"]) for cell in nb["cells"] if cell["cell_type"] == "code"]
    code = "\n".join(code_cells)

    tree = safe_parse(code, file_path)
    if tree is None:
        return set()  # Skip file if parsing fails

    imports = {node.names[0].name.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.Import)}
    imports |= {node.module.split('.')[0] for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}

    return imports


def get_dependencies(paths, output_file="requirements.txt"):
    """Find all Python and Notebook files, extract imports, and generate a requirements.txt."""
    dependencies = set()
    files_to_process = []

    for path in paths:
        if os.path.isdir(path):
            print(f"🔍 Searching in directory: {path}")
            files_to_process.extend(find_files(path))
        elif os.path.isfile(path) and (path.endswith(".py") or path.endswith(".ipynb")):
            files_to_process.append(path)
        else:
            print(f"⚠️ Skipping: {path} (not a valid Python or Jupyter file)")

    if not files_to_process:
        print("❌ No valid files found. Exiting.")
        return

    for file in files_to_process:
        if file.endswith(".py"):
            dependencies |= extract_imports_from_py(file)
        elif file.endswith(".ipynb"):
            dependencies |= extract_imports_from_ipynb(file)

    print("\n📦 Resolving package versions...\n")

    # Get installed versions
    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

    # Write to requirements.txt
    with open(output_file, "w") as f:
        for dep in sorted(dependencies):
            version = installed_packages.get(dep.lower(), "")
            if version:  # Only include dependencies that are installed
                f.write(f"{dep}=={version}\n")

    print(f"✅ Requirements saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Generate a requirements.txt file from Python and Jupyter Notebook files.")
    parser.add_argument("paths", nargs="+", help="Files or directories to process")
    parser.add_argument("-o", "--output", default="requirements.txt", help="Output file (default: requirements.txt)")

    args = parser.parse_args()
    get_dependencies(args.paths, args.output)

if __name__ == "__main__":
    main()
