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
from typing import Literal, TypedDict

import instructor
import numpy as np
import yaml
from openai import OpenAI
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ============================================================================
# Pydantic Schemas
# ============================================================================


class ActionItem(BaseModel):
    """Structured action item extracted from session summaries.

    Follows Instructor pattern for reliable LLM extraction with validation.
    """

    id: str = Field(description="Unique ID: {date}-{file}#{section}#{index}")
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
    related_files: list[str] = Field(default_factory=list, description="Mentioned file paths")
    blockers: list[str] | None = Field(default=None, description="Dependencies or blockers")


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

**Session:** {metadata["date"]} - {metadata["title"]}
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
                sections.append(
                    {
                        "header": current_header,
                        "content": "\n".join(current_content).strip(),
                    }
                )
            # Start new section
            current_header = header_match.group(1).strip()
            current_content = []
        else:
            current_content.append(line)

    # Save final section
    if current_content:
        sections.append(
            {
                "header": current_header,
                "content": "\n".join(current_content).strip(),
            }
        )

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
# Deduplication (Phase 3)
# ============================================================================


class DuplicatePair(TypedDict):
    """Pair of potentially duplicate items with similarity score."""

    item1: ActionItem
    item2: ActionItem
    similarity: float
    level: Literal["text", "semantic", "contextual"]


def compute_text_similarity(item1: ActionItem, item2: ActionItem) -> float:
    """Compute text similarity using TF-IDF and cosine similarity.

    Level 1: Fast filter for exact/near duplicates.

    Args:
        item1: First action item
        item2: Second action item

    Returns:
        Similarity score (0.0 to 1.0)
    """
    # Combine title and description for richer comparison
    text1 = f"{item1.title} {item1.description}"
    text2 = f"{item2.title} {item2.description}"

    # Handle empty strings - both empty should return 0.0 (not comparable)
    text1_clean = text1.strip()
    text2_clean = text2.strip()

    if not text1_clean or not text2_clean:
        return 0.0

    # If both are identical after cleaning, return 1.0
    if text1_clean == text2_clean:
        return 1.0

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer(lowercase=True, stop_words="english")
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except ValueError:
        # Handle edge case where vocabulary is empty (e.g., only stop words)
        # Both texts have no meaningful content after removing stop words
        # In this case, similarity is based on exact match
        if text1_clean.lower() == text2_clean.lower():
            return 1.0
        # Different texts with no content after stop word removal = different
        return 0.0


def compute_semantic_similarity(item1: ActionItem, item2: ActionItem, client: OpenAI) -> float:
    """Compute semantic similarity using LLM embeddings.

    Level 2: Semantic understanding beyond text matching.

    Args:
        item1: First action item
        item2: Second action item
        client: OpenAI client for embeddings

    Returns:
        Similarity score (0.0 to 1.0)
    """
    # Combine title and description
    text1 = f"{item1.title}. {item1.description}"
    text2 = f"{item2.title}. {item2.description}"

    # Get embeddings from OpenAI
    response = client.embeddings.create(input=[text1, text2], model="text-embedding-3-small")

    # Compute cosine similarity
    emb1 = np.array(response.data[0].embedding)
    emb2 = np.array(response.data[1].embedding)
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    return float(similarity)


def compute_contextual_similarity(item1: ActionItem, item2: ActionItem) -> float:
    """Compute contextual similarity based on initiative and file overlap.

    Level 3: Context-based heuristics.

    Args:
        item1: First action item
        item2: Second action item

    Returns:
        Similarity score (0.0 to 1.0)
    """
    # File overlap similarity (Jaccard index)
    files1 = set(item1.related_files or [])
    files2 = set(item2.related_files or [])

    if not files1 and not files2 or not files1 or not files2:
        file_similarity = 0.0
    else:
        intersection = len(files1 & files2)
        union = len(files1 | files2)
        file_similarity = intersection / union if union > 0 else 0.0

    # Category match (same category = higher similarity)
    category_match = 1.0 if item1.category == item2.category else 0.0

    # Impact match
    impact_match = 1.0 if item1.impact == item2.impact else 0.0

    # Weighted combination
    contextual_score = (file_similarity * 0.6) + (category_match * 0.3) + (impact_match * 0.1)

    return float(contextual_score)


def deduplicate_items(
    items: list[ActionItem],
    client: OpenAI | None = None,
    return_borderline: bool = False,
) -> list[ActionItem] | tuple[list[ActionItem], list[DuplicatePair]]:
    """Deduplicate action items using cascading similarity levels.

    Pipeline: Level 1 (text) → Level 2 (semantic) → Level 3 (contextual)

    Thresholds:
    - ≥0.95 text: Exact duplicate (merge)
    - ≥0.80 text: High confidence duplicate (merge)
    - 0.60-0.80 text: Medium confidence (flag for review)
    - <0.60 text: Check semantic similarity
    - ≥0.85 semantic: Semantic duplicate (merge)
    - 0.70-0.85 semantic: Medium confidence (flag for review)
    - <0.70 semantic: Check contextual similarity
    - ≥0.80 contextual: High file/initiative overlap (merge)

    Args:
        items: List of action items to deduplicate
        client: OpenAI client for semantic similarity (optional)
        return_borderline: If True, also return borderline pairs for review

    Returns:
        Deduplicated list of items, optionally with borderline pairs
    """
    if len(items) <= 1:
        return (items, []) if return_borderline else items

    # Track which items to keep and merge mappings
    keep_indices = set(range(len(items)))
    borderline_pairs: list[DuplicatePair] = []

    # Compare all pairs
    for i in range(len(items)):
        if i not in keep_indices:
            continue

        for j in range(i + 1, len(items)):
            if j not in keep_indices:
                continue

            item1 = items[i]
            item2 = items[j]

            # Level 1: Text similarity
            text_sim = compute_text_similarity(item1, item2)

            if text_sim >= 0.80:
                # High confidence duplicate - merge
                keep_indices.discard(j)
                if 0.60 <= text_sim < 0.80:
                    borderline_pairs.append(
                        DuplicatePair(item1=item1, item2=item2, similarity=text_sim, level="text")
                    )
                continue
            elif text_sim >= 0.60:
                # Borderline - flag for review
                borderline_pairs.append(
                    DuplicatePair(item1=item1, item2=item2, similarity=text_sim, level="text")
                )
                continue

            # Level 2: Semantic similarity (if API available)
            if client:
                try:
                    semantic_sim = compute_semantic_similarity(item1, item2, client)

                    if semantic_sim >= 0.85:
                        # Semantic duplicate - merge
                        keep_indices.discard(j)
                        continue
                    elif semantic_sim >= 0.70:
                        # Borderline semantic similarity
                        borderline_pairs.append(
                            DuplicatePair(
                                item1=item1,
                                item2=item2,
                                similarity=semantic_sim,
                                level="semantic",
                            )
                        )
                        continue
                except Exception as e:
                    print(f"   ⚠️  Semantic similarity error: {e}")

            # Level 3: Contextual similarity
            contextual_sim = compute_contextual_similarity(item1, item2)

            if contextual_sim >= 0.80:
                # High contextual overlap - likely duplicate
                keep_indices.discard(j)
            elif contextual_sim >= 0.60:
                # Borderline contextual similarity
                borderline_pairs.append(
                    DuplicatePair(
                        item1=item1,
                        item2=item2,
                        similarity=contextual_sim,
                        level="contextual",
                    )
                )

    # Return deduplicated items
    deduplicated = [items[i] for i in sorted(keep_indices)]

    if return_borderline:
        return deduplicated, borderline_pairs
    return deduplicated


def export_borderline_cases(borderline_pairs: list[DuplicatePair], output_path: Path) -> None:
    """Export borderline duplicate pairs for human review.

    Args:
        borderline_pairs: List of borderline duplicate pairs
        output_path: Path to YAML output file
    """
    export_data = {
        "review_required": len(borderline_pairs),
        "generated_at": datetime.now().isoformat(),
        "pairs": [
            {
                "similarity": pair["similarity"],
                "level": pair["level"],
                "item1": {
                    "id": pair["item1"].id,
                    "title": pair["item1"].title,
                    "description": pair["item1"].description,
                    "source": pair["item1"].source_summary,
                },
                "item2": {
                    "id": pair["item2"].id,
                    "title": pair["item2"].title,
                    "description": pair["item2"].description,
                    "source": pair["item2"].source_summary,
                },
            }
            for pair in borderline_pairs
        ],
    }

    output_path.write_text(yaml.dump(export_data, default_flow_style=False, sort_keys=False))
    print(f"📋 Borderline cases exported to: {output_path}")


# ============================================================================
# Initiative Mapping (Phase 4 - MVP)
# ============================================================================


def load_initiative_metadata(initiatives_dir: Path) -> list[dict[str, str]]:
    """Load basic metadata from initiative markdown files.

    MVP implementation for Phase 4. Returns initiative metadata for mapping.

    Args:
        initiatives_dir: Path to initiatives directory (active or completed)

    Returns:
        List of initiative metadata dicts with keys: title, status, path, related_files
    """
    initiatives = []

    if not initiatives_dir.exists():
        return initiatives

    for initiative_file in initiatives_dir.glob("*.md"):
        try:
            content = initiative_file.read_text()

            # Extract title (first # heading)
            title = ""
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line[2:].strip()
                    break

            # Extract status from frontmatter or content
            status = "Unknown"
            if "Status: Active" in content:
                status = "Active"
            elif "Status: Completed" in content:
                status = "Completed"

            # Extract related files (simple heuristic - look for file paths)
            related_files = []
            for line in content.split("\n"):
                # Look for paths like src/module.py or tests/test_*.py
                if ".py" in line and ("src/" in line or "tests/" in line or "scripts/" in line):
                    # Extract path between backticks or quotes
                    parts = line.split("`")
                    for part in parts:
                        if ".py" in part and ("/" in part or "\\" in part):
                            related_files.append(part.strip())

            initiatives.append(
                {
                    "title": title,
                    "status": status,
                    "path": str(initiative_file),
                    "related_files": related_files[:10],  # Limit to 10
                }
            )
        except Exception as e:
            print(f"   ⚠️  Error loading initiative {initiative_file.name}: {e}")
            continue

    return initiatives


def map_action_item_to_initiatives(
    item: ActionItem,
    initiatives: list[dict[str, str]],
) -> list[dict[str, float]]:
    """Map an action item to relevant initiatives based on file overlap.

    MVP implementation for Phase 4. Uses simple file overlap heuristic.
    Full semantic matching deferred to Phase 5 integration.

    Args:
        item: Action item to map
        initiatives: List of initiative metadata dicts

    Returns:
        List of matches with initiative title and overlap score (0.0-1.0)
    """
    matches = []
    item_files = set(item.related_files or [])

    if not item_files:
        return matches

    for initiative in initiatives:
        init_files = set(initiative.get("related_files", []))

        if not init_files:
            continue

        # Compute Jaccard similarity
        intersection = len(item_files & init_files)
        union = len(item_files | init_files)

        if union > 0:
            overlap_score = intersection / union

            if overlap_score > 0.0:
                matches.append(
                    {
                        "title": initiative["title"],
                        "status": initiative["status"],
                        "overlap_score": overlap_score,
                        "matching_files": list(item_files & init_files),
                    }
                )

    # Sort by overlap score descending
    matches.sort(key=lambda x: x["overlap_score"], reverse=True)

    return matches


def should_create_new_initiative(item: ActionItem, best_match_score: float = 0.0) -> bool:
    """Determine if action item warrants a new initiative.

    MVP heuristic for Phase 4:
    - High impact AND high confidence
    - No strong existing initiative match (score < 0.3)

    Args:
        item: Action item to evaluate
        best_match_score: Best overlap score from existing initiatives

    Returns:
        True if new initiative should be created
    """
    return item.impact == "high" and item.confidence == "high" and best_match_score < 0.3


# ============================================================================
# CLI Entry Point
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
