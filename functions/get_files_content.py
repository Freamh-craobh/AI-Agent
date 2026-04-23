import os
from config import MAX_CHARS 
from google.genai import types

debug = False  # Set to True to enable debug prints

def get_files_content(working_directory, file_path):
    try:
        full_path = os.path.normpath(os.path.join(os.path.abspath(working_directory), file_path))
        working_directory = os.path.normpath(os.path.abspath(working_directory))
        valid_file = os.path.commonpath([full_path, working_directory]) == working_directory
        if not valid_file:
            return str(f"Error: Cannot read {file_path} as it is outside the permitted working directory")
        if not os.path.isfile(full_path):
            return str(f"Error: File not found or is not a regular file: {file_path}")
        with open(full_path, "r") as f:
            str_content = f.read(MAX_CHARS)  # Read up to MAX_CHARS characters
            if f.read(1):  # Check if there's more content beyond the limit
                 str_content += f"[...File {file_path} truncated at {MAX_CHARS} characters]"
        if debug:
            return f"Debug success: {str_content[0:100]} + \n..."  # Print the first 100 characters for debugging   
        return str_content
    except Exception as e:
        return str(f"Error: {e}")

schema_get_files_content = types.FunctionDeclaration(
    name = "get_files_content",
    description = "Gets the content of a specified file",
    parameters = types.Schema(  
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read content from, relative to the working directory (default is the working directory itself)",
            )
        },
        required=["file_path"]
    )
)