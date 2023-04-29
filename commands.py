import json
import os

def open_file(file_path):
    try:
        with open(file_path, 'r') as file:
            jsonld_data = json.load(file)
            file_name = os.path.basename(file_path)
            print(f"File {file_name} has been opened successfully")
        return json.dumps(jsonld_data, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
