import json
def flatten_json(nested_json, parent_key=''):
    """
    Recursively flattens a nested JSON object into a dictionary with paths as keys.

    :param nested_json: The JSON object (Python dictionary) to flatten
    :param parent_key: The base key used for recursion, defaults to an empty string
    :return: A flattened dictionary with paths as keys
    """
    items = {}

    for key, value in nested_json.items():
        new_key = f"{parent_key}/{key}" if parent_key else f"/{key}"

        if isinstance(value, dict):
            # If the value is a dict, recurse
            items.update(flatten_json(value, new_key))
        else:
            # If the value is not a dict, just add it to the result
            items[new_key] = value

    return items


def is_valid_json(json_string):
    """
    Check if a given string is valid JSON.

    :param json_string: The string to check
    :return: True if valid JSON, False otherwise
    """
    try:
        json.loads(json_string)  # Attempt to parse the JSON string
        return True
    except json.JSONDecodeError:
        return False  # If a JSONDecodeError is raised, the string is not valid JSON

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return None

def dict_to_json(znode_name,dict):

    znode_name="root_" if znode_name == "/" else znode_name.replace("/", "_")

    with open(f"{znode_name}znode_backup.json", "w") as outfile:
        json.dump(dict, outfile, indent = 4)