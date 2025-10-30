import os
from pathlib import Path

def count_tokens_in_file(filepath):
    """Estimates the number of tokens in a file."""
    with open(filepath, 'r') as f:
        content = f.read()
    return len(content) / 4

def main():
    """Main function to count tokens in .unified directory."""
    unified_dir = Path(".unified")
    all_files = []

    for root, _, files in os.walk(unified_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = Path(root) / file
                all_files.append((filepath, count_tokens_in_file(filepath)))

    all_files.sort(key=lambda x: x[1], reverse=True)

    print("# Token Inventory")
    print("\n## Top 10 Heaviest Files")
    print("| File | Estimated Tokens |")
    print("|---|---|")
    for filepath, tokens in all_files[:10]:
        print(f"| {filepath} | {tokens:.0f} |")

    print("\n## Full Inventory")
    print("| File | Estimated Tokens |")
    print("|---|---|")
    total_tokens = 0
    for filepath, tokens in all_files:
        print(f"| {filepath} | {tokens:.0f} |")
        total_tokens += tokens

    print(f"\n**Total Estimated Tokens:** {total_tokens:.0f}")

if __name__ == "__main__":
    main()
