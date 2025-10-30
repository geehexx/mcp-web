import os
from pathlib import Path
import yaml

def get_frontmatter_keys(filepath):
    """Extracts the keys from the YAML frontmatter of a file."""
    with open(filepath, 'r') as f:
        content = f.read()

    try:
        # Split the content to get the frontmatter
        if content.startswith('---'):
            parts = content.split('---')
            if len(parts) > 2:
                frontmatter = yaml.safe_load(parts[1])
                if isinstance(frontmatter, dict):
                    return frontmatter.keys()
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in {filepath}: {e}")

    return []

def main():
    """Main function to catalog frontmatter keys."""
    unified_dir = Path(".unified")
    all_files = []
    all_keys = set()
    file_key_map = {}

    for root, _, files in os.walk(unified_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = Path(root) / file
                keys = get_frontmatter_keys(filepath)
                all_keys.update(keys)
                file_key_map[str(filepath)] = set(keys)

    sorted_keys = sorted(list(all_keys))

    print("# Frontmatter Field Matrix")
    print("\nThis matrix shows which frontmatter fields are used in each file.")

    header = "| File | " + " | ".join(sorted_keys) + " |"
    print(header)

    separator = "|---|" + "---|"*len(sorted_keys)
    print(separator)

    for filepath, keys in sorted(file_key_map.items()):
        row = f"| {filepath} |"
        for key in sorted_keys:
            if key in keys:
                row += " ✓ |"
            else:
                row += "   |"
        print(row)

if __name__ == "__main__":
    main()
