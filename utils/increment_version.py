import json
import os

def increment_version():
    # Determine the project root directory
    # This script is in utils/, so root is parent
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)
    version_file = os.path.join(root_dir, 'frontend', 'version.json')

    if not os.path.exists(version_file):
        print(f"Error: {version_file} not found.")
        # Create it with default version if missing
        os.makedirs(os.path.dirname(version_file), exist_ok=True)
        with open(version_file, 'w') as f:
            json.dump({"version": "1.0.0"}, f, indent=2)
        print(f"Created {version_file} with version 1.0.0")
        return

    with open(version_file, 'r+') as f:
        data = json.load(f)
        v_parts = data['version'].split('.')
        # Increment the patch version
        v_parts[-1] = str(int(v_parts[-1]) + 1)
        new_version = '.'.join(v_parts)
        data['version'] = new_version
        
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()
        print(f"Incremented version to {new_version}")

if __name__ == "__main__":
    increment_version()
