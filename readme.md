Here’s a **README.md** that explains the capabilities of your tool, including all the requested features like skipping `.dot` folders, handling broken files, and more.

---

# Python & Jupyter Notebook Dependency Extractor

This tool helps you generate a `requirements.txt` file by extracting all the **imported dependencies** from Python (`.py`) and Jupyter Notebook (`.ipynb`) files. It works by recursively searching for Python and notebook files in a given directory (or multiple files), extracting all used packages, and then resolving their versions from the environment.

## Features

- **Recursive Search**: Searches for `.py` and `.ipynb` files in the provided directory and subdirectories.
- **Handles Multiple Files**: Accepts both individual file paths and directories, and can process multiple files at once.
- **Skipping Hidden Directories**: Ignores directories that start with a dot (`.`) like `.git`, `.vscode`, etc.
- **Graceful Error Handling**:
  - **Malformed or Incomplete Python Code**: Skips files with syntax errors (e.g., incomplete statements).
  - **Corrupted or Empty Jupyter Notebooks**: Skips invalid or empty notebook files with appropriate error messages.
- **Version Resolution**: Extracts package versions from your current environment and generates the `requirements.txt` file with the correct versions.

## Installation

Clone this repository or download the Python script to use it:

```bash
git clone https://github.com/your-repository-url
cd your-repository
```

### Requirements

Ensure you have the following installed:
- Python 3.6 or later
- Required Python packages (can be installed automatically by `requirements.txt`).

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

You can run the script from the command line. The tool accepts a **directory**, **single file**, or **multiple files** as arguments. It will search for Python (`.py`) and Jupyter Notebook (`.ipynb`) files in the provided directory or process individual files.

```bash
python dep.py <path1> <path2> ... [-o OUTPUT_FILE]
```

- `<path1> <path2> ...`: Path(s) to the directory or files to process. You can provide multiple paths (directories or files).
- `-o OUTPUT_FILE`: Optional flag to specify the output `requirements.txt` file (default is `requirements.txt`).

### Examples:

1. **Process a single Python file**:
    ```bash
    python dep.py my_script.py
    ```

2. **Process multiple files**:
    ```bash
    python dep.py my_script.py my_notebook.ipynb
    ```

3. **Process a directory and its subdirectories**:
    ```bash
    python dep.py /path/to/directory
    ```

4. **Specify output file name**:
    ```bash
    python dep.py /path/to/directory -o custom_requirements.txt
    ```

### How It Works:

1. **File Discovery**: The tool will recursively search the provided directories for Python (`.py`) and Jupyter Notebook (`.ipynb`) files. It will **ignore hidden directories** (those starting with a dot, e.g., `.git`, `.vscode`).
2. **Dependency Extraction**: For each valid file, it extracts the imported libraries. For Python files, it parses the code using the `ast` module. For notebooks, it reads the notebook's cells and parses the code.
3. **Error Handling**:
   - **Malformed Python Code**: Files with syntax errors (e.g., incomplete statements like `w=`) are skipped with a warning.
   - **Corrupted Notebooks**: If a notebook is empty or corrupted (e.g., invalid JSON), it will be skipped with an error message.
4. **Version Resolution**: The script checks the installed packages in your current environment and includes the correct versions in the `requirements.txt`.
5. **Output**: Finally, it generates the `requirements.txt` file with the dependencies and their versions.

## Notes

- The script uses the **`pkg_resources`** library to fetch package versions, ensuring that the `requirements.txt` reflects the exact versions of libraries in your environment.
- If a file is skipped due to errors (e.g., incomplete code or corrupted notebook), the script will **continue processing other files**.

## Example Output

```bash
📂 Processing: /path/to/script.py
📓 Processing: /path/to/notebook.ipynb
⚠️ Skipping malformed code in: /path/to/broken_script.py (SyntaxError: invalid syntax)
⚠️ Skipping malformed or empty notebook: /path/to/broken_notebook.ipynb (Error: Expecting value: line 1 column 1 (char 0))

📦 Resolving package versions...

✅ Requirements saved to requirements.txt
```

The `requirements.txt` will look like this:

```txt
numpy==1.23.1
pandas==1.4.2
matplotlib==3.4.3
```

## Troubleshooting

- **Encoding Errors**: If a Python file contains special characters that cannot be decoded as UTF-8, the script will attempt to decode it using `latin-1` encoding. If both attempts fail, the file will be skipped.
- **Empty or Invalid Notebooks**: If a notebook is empty or cannot be parsed due to invalid JSON, it will be skipped.

## Contributing

If you find any bugs or have ideas for new features, feel free to open an issue or submit a pull request!

---

This tool will make your workflow of generating and managing Python project dependencies much smoother! 😎
