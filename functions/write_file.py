import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        working_directory = os.path.normpath(os.path.abspath(working_directory))
        valid_file = os.path.commonpath([full_path, working_directory]) == working_directory
        if not valid_file:
            return str(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(full_path):
            return str(f'Error: Cannot write to "{file_path}" as it is a directory')
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return str(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return str(f"Error: {e}")   

schema_write_file = types.FunctionDeclaration(
    name = "write_file",
    description = "Writes content to a specified file",
    parameters = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write content to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            )
        },
        required=["file_path", "content"]
    )
)