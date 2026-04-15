#todo
import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.normpath(os.path.join(os.path.abspath(working_directory), directory))
        working_directory = os.path.normpath(os.path.abspath(working_directory))
        #print(working_directory)
        valid_dir = os.path.commonpath([full_path, working_directory]) == working_directory
        if not valid_dir:
            return str(f"Error: Cannot list {directory} as it is outside the permitted working directory")
        if not os.path.isdir(full_path):
            return str(f"Error: {directory} is not a directory")
        items = []
        for file in os.listdir(full_path):
            name = os.path.basename(file)
            size = os.path.getsize(os.path.join(full_path, file))
            is_dir = os.path.isdir(os.path.join(full_path, file))
            items.append(f"- {name}: file_size={size}, is_dir={is_dir}")
        return "\n".join(items) + "\n"
    except Exception as e:
        return str(f"Error: {e}")
