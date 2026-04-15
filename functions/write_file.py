import os

def write_file(working_path, file_path, content):
    try:
        full_path = os.path.normpath(os.path.join(os.path.abspath(working_path), file_path))
        working_path = os.path.normpath(os.path.abspath(working_path))
        valid_file = os.path.commonpath([full_path, working_path]) == working_path
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
