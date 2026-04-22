import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        full_path = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        working_directory = os.path.normpath(os.path.abspath(working_directory))
        valid_file = os.path.commonpath([full_path, working_directory]) == working_directory
        if not valid_file:
            return str(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(full_path):
            return str(f'Error: "{file_path}" does not exist or is not a regular file')
        if ".py" not in full_path:
            return str(f'Error: "{file_path}" is not a Python file')
        command = ["python", full_path]
        if args:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, cwd=working_directory, timeout=30)
        if result.returncode != 0:
            return str(f'Error: "Process exited with code {result.returncode}"')
        if not result.stderr and not result.stdout:
            return str("No output produced")
        output_str = f"STDOUT: {result.stdout} \n" + f"STDERR: {result.stderr}"
        return output_str
    except Exception as e:
        return str(f"Error: executing Python file: {e}")
    

schema_run_python_file = types.FunctionDeclaration(
    name = "run_python_file",
    description = "Runs a Python file",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python script",
            )
        },
        required=["file_path"]
    )
)