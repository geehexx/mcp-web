#!/usr/bin/env python3
"""Extract action items from session summaries using structured LLM extraction.

Phase 2 implementation of Session Summary Mining initiative:
- Pydantic schemas for structured extraction with validation
- Section-based extraction for granular context preservation
- Instructor pattern for reliable LLM interaction
- SQLite logging for quality tracking and analysis
- YAML output (30% more token-efficient than JSON)

Usage:
    # Extract from single file
    python scripts/extract_action_items_v2.py docs/archive/session-summaries/2025-10-20-*.md

    # Extract from date range
    python scripts/extract_action_items_v2.py --date-range 2025-10-15:2025-10-20

    # Extract from all summaries
    python scripts/extract_action_items_v2.py --all --output action-items.yaml
"""

import argparse
import re
import sqlite3
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Literal

import instructor
import yaml
from openai import OpenAI
from pydantic import BaseModel, Field

# ============================================================================
# Pydantic Schemas
# ============================================================================


class ActionItem(BaseModel):
    """Structured action item extracted from session summaries.

    Follows Instructor pattern for reliable LLM extraction with validation.
    """

    id: str = Field(
        description="Unique ID: {date}-{file}#{section}#{index}"
    )
    title: str = Field(description="Concise title (5-10 words)")
    description: str = Field(description="Detailed description (1-3 sentences)")
    category: Literal[
        "missing_capability",
        "pain_point",
        "regression",
        "improvement",
        "technical_debt",
        "documentation",
        "testing",
        "automation",
        "security",
        "performance",
    ] = Field(description="Primary category")
    impact: Literal["high", "medium", "low"] = Field(
        description="Estimated impact on project success"
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="Confidence in extraction accuracy"
    )
    source_summary: str = Field(description="Source filename")
    source_section: str = Field(description="Section header where found")
    session_date: date = Field(description="Session date from filename")
    related_files: list[str] = Field(
        default_factory=list, description="Mentioned file paths"
    )
    blockers: list[str] | None = Field(
        default=None, description="Dependencies or blockers"
    )


# ============================================================================
# Extraction Prompts
# ============================================================================


SYSTEM_PROMPT = """You are an expert at extracting actionable insights from technical session summaries.

Identify:
1. **Missing Capabilities** - Features/tools that don't exist yet
2. **Pain Points** - Friction, inefficiencies, manual work
3. **Regressions** - Things that broke or got worse
4. **Improvements** - Optimization opportunities
5. **Technical Debt** - Code quality issues
6. **Documentation Gaps** - Missing or outdated docs
7. **Testing Gaps** - Untested scenarios
8. **Automation Opportunities** - Repetitive manual tasks
9. **Security Issues** - Vulnerabilities, compliance gaps
10. **Performance Issues** - Slow operations

**Classification:**
- Impact: High (blocks work), Medium (improves productivity), Low (nice-to-have)
- Confidence: High (explicit mention), Medium (implied), Low (uncertain)

**Rules:**
- Extract concrete, actionable items (not generic observations)
- Preserve context (quote key phrases)
- Include file paths mentioned
- Note blockers if mentioned
- Skip completed items (✅ or "Done")
"""


def create_user_prompt(section_header: str, section_content: str, metadata: dict[str, str]) -> str:
    """Create extraction prompt for a specific section."""
    return f"""Extract action items from this session summary section:

**Session:** {metadata['date']} - {metadata['title']}
**Section:** {section_header}

**Content:**
```
{section_content}
```

Return action items as a list. If none found, return empty list."""


# ============================================================================
# Section Parsing
# ============================================================================


def parse_markdown_sections(content: str) -> list[dict[str, str]]:
    """Parse markdown into sections by headers.

    Args:
        content: Full markdown content

    Returns:
        List of dicts with 'header' and 'content' keys
    """
    sections = []
    current_header = "Introduction"
    current_content = []

    for line in content.split("\n"):
        # Match markdown headers (## or ###)
        header_match = re.match(r"^#{2,3}\s+(.+)$", line)
        if header_match:
            # Save previous section
            if current_content:
                sections.append({
                    "header": current_header,
                    "content": "\n".join(current_content).strip(),
                })
            # Start new section
            current_header = header_match.group(1).strip()
            current_content = []
        else:
            current_content.append(line)

    # Save final section
    if current_content:
        sections.append({
            "header": current_header,
            "content": "\n".join(current_content).strip(),
        })

    return sections


def should_skip_section(header: str) -> bool:
    """Skip sections unlikely to contain action items."""
    skip_patterns = [
        "table of contents",
        "metadata",
        "files changed",
        "commits",
        "git log",
    ]
    return any(pattern in header.lower() for pattern in skip_patterns)


def extract_date_from_filename(filename: str) -> date:
    """Extract date from filename (format: YYYY-MM-DD-*.md)."""
    date_match = re.match(r"(\d{4})-(\d{2})-(\d{2})", filename)
    if date_match:
        year, month, day = map(int, date_match.groups())
        return date(year, month, day)
    return date.today()


def extract_title(content: str) -> str:
    """Extract title from markdown (first # header)."""
    for line in content.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


# ============================================================================
# Extraction Pipeline
# ============================================================================


def extract_from_section(
    client: instructor.Instructor,
    section: dict[str, str],
    metadata: dict[str, str],
) -> list[ActionItem]:
    """Extract action items from a single section.

    Args:
        client: Instructor client for LLM calls
        section: Section dict with header and content
        metadata: Summary metadata (date, title, filename)

    Returns:
        List of extracted action items
    """
    try:
        prompt = create_user_prompt(section["header"], section["content"], metadata)

        items = client.chat.completions.create(
            model="gpt-4o-mini",  # Fast, cheap for extraction
            response_model=list[ActionItem],
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,  # Low temperature for consistency
        )

        # Add source metadata and generate IDs
        for i, item in enumerate(items, 1):
            if not item.source_summary:
                item.source_summary = metadata["filename"]
            if not item.source_section:
                item.source_section = section["header"]
            if not item.session_date:
                item.session_date = metadata["date"]
            # Generate ID if not set
            if not item.id or item.id == "":
                date_str = metadata["date"].isoformat()
                file_slug = metadata["filename"].replace(".md", "")
                section_slug = re.sub(r"[^a-z0-9]+", "-", section["header"].lower())
                item.id = f"{date_str}-{file_slug}#{section_slug}#{i}"

        return items

    except Exception as e:
        print(f"   ⚠️  Extraction error in section '{section['header']}': {e}")
        return []


def extract_from_summary(client: instructor.Instructor, file_path: Path) -> list[ActionItem]:
    """Extract all action items from a summary file.

    Args:
        client: Instructor client
        file_path: Path to session summary

    Returns:
        List of all extracted action items
    """
    # Read and parse summary
    content = file_path.read_text()
    sections = parse_markdown_sections(content)

    # Extract metadata
    metadata = {
        "filename": file_path.name,
        "date": extract_date_from_filename(file_path.name),
        "title": extract_title(content),
    }

    # Extract from each section
    all_items = []
    for section in sections:
        if should_skip_section(section["header"]):
            continue
        if len(section["content"]) < 50:  # Skip very short sections
            continue

        items = extract_from_section(client, section, metadata)
        all_items.extend(items)

    return all_items


# ============================================================================
# SQLite Logging
# ============================================================================


def init_database(db_path: Path) -> None:
    """Initialize SQLite database for extraction logging."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extractions (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            summary_file TEXT NOT NULL,
            session_date TEXT NOT NULL,
            section TEXT NOT NULL,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            impact TEXT NOT NULL,
            confidence TEXT NOT NULL,
            description TEXT,
            related_files TEXT,
            blockers TEXT
        )
    """)

    conn.commit()
    conn.close()


def log_extraction(db_path: Path, items: list[ActionItem]) -> None:
    """Log extracted items to SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for item in items:
        cursor.execute(
            """
            INSERT OR REPLACE INTO extractions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.id,
                datetime.now().isoformat(),
                item.source_summary,
                item.session_date.isoformat(),
                item.source_section,
                item.title,
                item.category,
                item.impact,
                item.confidence,
                item.description,
                ",".join(item.related_files) if item.related_files else None,
                ",".join(item.blockers) if item.blockers else None,
            ),
        )

    conn.commit()
    conn.close()


# ============================================================================
# CLI Interface
# ============================================================================


def find_summaries_by_date_range(start_date: date, end_date: date) -> list[Path]:
    """Find session summaries within date range."""
    summaries_dir = Path("docs/archive/session-summaries")
    if not summaries_dir.exists():
        print(f"❌ Error: Directory not found: {summaries_dir}")
        return []

    matching_files = []
    for file_path in summaries_dir.glob("*.md"):
        try:
            file_date = extract_date_from_filename(file_path.name)
            if start_date <= file_date <= end_date:
                matching_files.append(file_path)
        except ValueError:
            continue

    return sorted(matching_files)


def parse_date_range(date_range_str: str) -> tuple[date, date]:
    """Parse date range string (format: YYYY-MM-DD:YYYY-MM-DD)."""
    try:
        start_str, end_str = date_range_str.split(":")
        start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError("Start date must be before end date")

        return start_date, end_date
    except Exception as e:
        raise ValueError("Invalid date range format. Use YYYY-MM-DD:YYYY-MM-DD") from e


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract action items from session summaries using structured LLM extraction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("files", nargs="*", help="Session summary files to process")
    parser.add_argument("--date-range", help="Extract from date range (YYYY-MM-DD:YYYY-MM-DD)")
    parser.add_argument("--all", action="store_true", help="Process all session summaries")
    parser.add_argument("--output", "-o", type=Path, help="Output file for extracted items (YAML)")
    parser.add_argument("--db", type=Path, default="extractions.db", help="SQLite database path")

    args = parser.parse_args()

    # Determine which files to process
    file_paths: list[Path] = []

    if args.all:
        summaries_dir = Path("docs/archive/session-summaries")
        if summaries_dir.exists():
            file_paths = sorted(summaries_dir.glob("*.md"))
        else:
            print(f"❌ Error: Directory not found: {summaries_dir}")
            return 1

    elif args.date_range:
        try:
            start_date, end_date = parse_date_range(args.date_range)
            print(f"📅 Searching for summaries from {start_date} to {end_date}")
            file_paths = find_summaries_by_date_range(start_date, end_date)

            if not file_paths:
                print("❌ No session summaries found in date range")
                return 1

            print(f"✅ Found {len(file_paths)} summaries")

        except ValueError as e:
            print(f"❌ Error: {e}")
            return 1

    elif args.files:
        for file_arg in args.files:
            path = Path(file_arg)
            if path.exists():
                file_paths.append(path)
            else:
                print(f"⚠️  Warning: File not found: {file_arg}")
    else:
        parser.print_help()
        return 1

    if not file_paths:
        print("❌ No valid files to process")
        return 1

    # Initialize database
    init_database(args.db)

    # Initialize Instructor client
    client = instructor.from_openai(OpenAI())

    # Process summaries
    print(f"\n🔍 Extracting action items from {len(file_paths)} summaries...\n")

    all_items = []
    for i, file_path in enumerate(file_paths, 1):
        print(f"[{i}/{len(file_paths)}] Processing: {file_path.name}")

        try:
            items = extract_from_summary(client, file_path)
            all_items.extend(items)

            # Log to database
            log_extraction(args.db, items)

            print(f"   ✅ Extracted {len(items)} items")

        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

    # Output results
    print(f"\n✅ Total extracted: {len(all_items)} action items")
    print(f"📊 Logged to database: {args.db}")

    if args.output:
        # Export to YAML (30% more token-efficient)
        output_data = {
            "generated_at": datetime.now().isoformat(),
            "source_files": [f.name for f in file_paths],
            "total_items": len(all_items),
            "action_items": [item.model_dump() for item in all_items],
        }

        args.output.write_text(yaml.dump(output_data, default_flow_style=False, sort_keys=False))
        print(f"💾 Exported to: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
