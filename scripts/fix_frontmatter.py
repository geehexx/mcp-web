#!/usr/bin/env python3
"""
Fix Windsurf frontmatter to minimal compatible format.

Removes custom fields and apostrophes, keeping only description.
"""

import re
import sys
from pathlib import Path
from typing import Tuple

def extract_frontmatter(content: str) -> Tuple[str, str, str]:
    """Extract frontmatter, body, and description from markdown content."""
    # Match YAML frontmatter
    fm_pattern = r'^---\n(.*?)\n---\n(.*)$'
    match = re.match(fm_pattern, content, re.DOTALL)
    
    if not match:
        return "", content, ""
    
    frontmatter = match.group(1)
    body = match.group(2)
    
    # Extract description
    desc_match = re.search(r'^description:\s*(.+?)$', frontmatter, re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else ""
    
    # Remove quotes if present
    description = description.strip('"').strip("'")
    
    return frontmatter, body, description


def clean_description(desc: str) -> str:
    """Remove apostrophes and clean description."""
    # Replace possessive apostrophes
    desc = desc.replace("Windsurf's", "Windsurf")
    desc = desc.replace("'s", "s")
    desc = desc.replace("'", "")
    desc = desc.replace('"', '')
    
    # Simplify for YAML safety
    desc = desc.replace("  ", " ")
    desc = desc.strip()
    
    # Ensure not too long
    if len(desc) > 200:
        desc = desc[:197] + "..."
    
    return desc


def create_minimal_frontmatter(description: str) -> str:
    """Create minimal Windsurf-compatible frontmatter."""
    clean_desc = clean_description(description)
    return f"---\ndescription: {clean_desc}\n---"


def process_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single file."""
    try:
        content = filepath.read_text(encoding='utf-8')
        old_fm, body, description = extract_frontmatter(content)
        
        if not description:
            print(f"⚠️  {filepath}: No description found, skipping")
            return False
        
        # Create new content
        new_frontmatter = create_minimal_frontmatter(description)
        new_content = f"{new_frontmatter}\n{body}"
        
        if dry_run:
            print(f"✓ {filepath}")
            print(f"  OLD: {description[:80]}...")
            print(f"  NEW: {clean_description(description)[:80]}...")
        else:
            filepath.write_text(new_content, encoding='utf-8')
            print(f"✅ Updated: {filepath}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fix Windsurf frontmatter format")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--path", default=".windsurf", help="Base path to search")
    args = parser.parse_args()
    
    base_path = Path(args.path)
    
    if not base_path.exists():
        print(f"❌ Path not found: {base_path}", file=sys.stderr)
        sys.exit(1)
    
    # Find all markdown files in rules and workflows
    rules_files = list((base_path / "rules").glob("*.md"))
    workflow_files = list((base_path / "workflows").glob("*.md"))
    
    all_files = rules_files + workflow_files
    
    print(f"Found {len(all_files)} files ({len(rules_files)} rules, {len(workflow_files)} workflows)")
    
    if args.dry_run:
        print("\n🔍 DRY RUN MODE - No files will be modified\n")
    
    success_count = 0
    for filepath in sorted(all_files):
        if process_file(filepath, dry_run=args.dry_run):
            success_count += 1
    
    print(f"\n✨ Processed {success_count}/{len(all_files)} files successfully")
    
    if args.dry_run:
        print("\nRun without --dry-run to apply changes")


if __name__ == "__main__":
    main()
