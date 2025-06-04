import json
import os

def save_data(data, filepath):
    # Overwrites existing content
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def load_data(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)
