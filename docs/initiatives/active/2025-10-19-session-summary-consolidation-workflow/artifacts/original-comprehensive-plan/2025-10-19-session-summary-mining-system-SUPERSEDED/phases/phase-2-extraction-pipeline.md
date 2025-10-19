# Phase 2: Extraction Pipeline Design

**Status:** Ready to Start
**Duration:** 4-5 hours
**Dependencies:** Phase 1 complete
**Deliverable:** Technical design document + prototype extraction script

---

## Objective

Design and prototype the extraction pipeline that converts session summaries into structured action items using Pydantic schemas and LLM-based extraction.

---

## Tasks

### 2.1 Define Pydantic Schema (1 hour)

Create `ActionItem` schema based on research (Instructor pattern):

```python
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import date

class ActionItem(BaseModel):
    """Single action item extracted from session summary."""

    # Identification
    id: str = Field(description="Unique ID: {source_file}#{section}#{index}")
    title: str = Field(description="Concise action item title (5-10 words)")
    description: str = Field(description="Detailed description with context")

    # Classification
    category: Literal[
        "workflow", "testing", "documentation", "security",
        "performance", "automation", "infrastructure", "quality"
    ] = Field(description="Primary category")

    impact: Literal["high", "medium", "low"] = Field(
        description="Potential impact if implemented"
    )

    confidence: Literal["high", "medium", "low"] = Field(
        description="Confidence in extraction accuracy and importance"
    )

    # Source tracking
    source_summary: str = Field(description="Source filename")
    source_section: str = Field(description="Section where found")
    source_quote: Optional[str] = Field(description="Verbatim quote if available")
    session_date: date = Field(description="Session date from filename")

    # Context
    related_files: List[str] = Field(
        default_factory=list,
        description="Files mentioned in relation to this item"
    )

    related_initiatives: List[str] = Field(
        default_factory=list,
        description="Initiatives mentioned in context"
    )

    # Dependencies & Blockers
    blockers: Optional[List[str]] = Field(
        default=None,
        description="What blocks this action item"
    )

    dependencies: Optional[List[str]] = Field(
        default=None,
        description="What this depends on"
    )

    # Initiative Mapping (populated later)
    suggested_initiative: Optional[str] = Field(
        default=None,
        description="Suggested initiative to add this to"
    )

    create_new_initiative: bool = Field(
        default=False,
        description="Whether this warrants a new initiative"
    )
```

**Success Criteria:**

- Schema validates correctly with Pydantic
- All required fields have descriptions
- Enums cover all observed categories from summaries

---

### 2.2 Design Extraction Prompts (1.5 hours)

#### System Prompt Template

```
You are an expert at analyzing software development session summaries to extract actionable items.

Your task is to identify:
1. **Pain points** - Problems explicitly mentioned or implied
2. **Missing capabilities** - Features/workflows identified as needed
3. **Regressions** - Issues that recurred or weren't fully fixed
4. **Improvement opportunities** - Suggestions or ideas mentioned

For each item, classify:
- **Impact**: High (blocks work or affects quality), Medium (improves efficiency), Low (nice-to-have)
- **Confidence**: High (explicitly stated 3+ times or user directive), Medium (mentioned 1-2 times), Low (implied or inferred)

Context preservation is critical - include section name, related files, and verbatim quotes when available.

Output format: Structured JSON matching the ActionItem schema.
```

#### User Prompt Template

```
Extract action items from the following session summary section:

**Session:** {session_date} - {session_title}
**Section:** {section_name}
**Content:**
```

{section_content}

```

Identify all pain points, missing capabilities, regressions, and improvement opportunities.
For each, provide: title, description, category, impact, confidence, source tracking, and context.
```

**Prompt Engineering Strategies:**

1. **Section-based extraction** - Process per section to preserve context boundaries
2. **Few-shot examples** - Include 2-3 example extractions for calibration
3. **Explicit classification** - Define impact/confidence criteria clearly
4. **Context preservation** - Require source quotes and related file mentions
5. **Iterative refinement** - Use chain-of-thought for complex extractions

---

### 2.3 Implement Extraction Pipeline (2 hours)

#### Pipeline Architecture

```
Input: Session Summary Files
    ↓
Stage 1: Preprocessing
    - Parse markdown structure
    - Extract metadata (date, title, focus)
    - Split into sections
    ↓
Stage 2: Section-Level Extraction
    - For each section:
        - Extract action items (LLM + Pydantic)
        - Validate structure
        - Log extraction
    ↓
Stage 3: Post-Processing
    - Deduplicate within summary
    - Add source references
    - Calculate derived fields
    ↓
Stage 4: Logging & Storage
    - Log to SQLite
    - Export to YAML
    - Generate extraction report
    ↓
Output: Structured Action Items (YAML)
```

#### Core Implementation

```python
# scripts/extract_action_items.py

import instructor
from openai import OpenAI
from pathlib import Path
from typing import List, Dict
import yaml
import sqlite3
from datetime import datetime

# Initialize client
client = instructor.from_openai(OpenAI())

def parse_summary(file_path: Path) -> Dict:
    """Parse summary into structured sections."""
    content = file_path.read_text()

    # Extract metadata from frontmatter or filename
    metadata = {
        "file": file_path.name,
        "date": extract_date_from_filename(file_path.name),
        "title": extract_title(content)
    }

    # Split by markdown headers
    sections = split_by_headers(content)

    return {"metadata": metadata, "sections": sections}

def extract_from_section(
    section: Dict,
    metadata: Dict
) -> List[ActionItem]:
    """Extract action items from a single section."""

    prompt = f"""
    Extract action items from the following session summary section:

    **Session:** {metadata['date']} - {metadata['title']}
    **Section:** {section['header']}
    **Content:**
    ```
    {section['content']}
    ```

    Identify all pain points, missing capabilities, regressions, and improvements.
    """

    try:
        items = client.chat.completions.create(
            model="gpt-4-turbo",
            response_model=List[ActionItem],
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2  # Low temperature for consistency
        )

        # Add source metadata
        for item in items:
            item.source_summary = metadata['file']
            item.source_section = section['header']
            item.session_date = metadata['date']

        return items

    except Exception as e:
        log_extraction_error(metadata, section, e)
        return []

def extract_from_summary(file_path: Path) -> List[ActionItem]:
    """Extract all action items from a summary."""

    parsed = parse_summary(file_path)
    all_items = []

    for section in parsed['sections']:
        # Skip low-value sections
        if should_skip_section(section['header']):
            continue

        items = extract_from_section(section, parsed['metadata'])
        all_items.extend(items)

    # Deduplicate within summary
    deduplicated = deduplicate_items(all_items, level="intra-summary")

    return deduplicated

def should_skip_section(header: str) -> bool:
    """Skip sections unlikely to contain action items."""
    skip_patterns = [
        "Table of Contents",
        "Executive Summary",  # Usually outcomes, not actionable gaps
        "Metadata",
        "Files Changed",
        "Commits"
    ]
    return any(pattern.lower() in header.lower() for pattern in skip_patterns)

def log_extraction(items: List[ActionItem], summary_file: str):
    """Log extraction to SQLite for analysis."""

    conn = sqlite3.connect("extractions.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS extractions (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            summary_file TEXT,
            action_item TEXT,
            category TEXT,
            impact TEXT,
            confidence TEXT
        )
    """)

    for item in items:
        cursor.execute("""
            INSERT OR REPLACE INTO extractions VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            item.id,
            datetime.now().isoformat(),
            summary_file,
            item.model_dump_json(),
            item.category,
            item.impact,
            item.confidence
        ))

    conn.commit()
    conn.close()

# CLI entry point
if __name__ == "__main__":
    import sys

    summary_file = Path(sys.argv[1])
    items = extract_from_summary(summary_file)

    # Output as YAML (30% more token-efficient)
    output = {
        "source": summary_file.name,
        "extracted_at": datetime.now().isoformat(),
        "action_items": [item.model_dump() for item in items]
    }

    print(yaml.dump(output, default_flow_style=False, sort_keys=False))

    # Log for analysis
    log_extraction(items, summary_file.name)
```

---

### 2.4 Create Test Cases (0.5 hours)

#### Test Strategy

1. **Unit Tests** - Schema validation, parsing functions
2. **Integration Tests** - End-to-end extraction on sample summaries
3. **Golden Tests** - Compare extraction against manually curated ground truth

#### Sample Test Cases

```python
# tests/test_extraction.py

def test_action_item_schema_validation():
    """Schema accepts valid items and rejects invalid."""
    valid_item = ActionItem(
        id="2025-10-18-summary#improvements#1",
        title="Add task format validation",
        description="Create pre-commit hook to validate task formatting",
        category="quality",
        impact="high",
        confidence="high",
        source_summary="2025-10-18-task-system-violations.md",
        source_section="Recommendations",
        session_date=date(2025, 10, 18)
    )
    assert valid_item.id.startswith("2025-10-18")

    # Test required fields
    with pytest.raises(ValidationError):
        ActionItem(title="No description")  # Missing required fields

def test_extract_from_known_summary():
    """Extract action items from a summary with known ground truth."""
    summary_file = Path("tests/fixtures/2025-10-18-task-system-violations.md")

    items = extract_from_summary(summary_file)

    # Should extract task validation recommendation
    task_validation_items = [
        item for item in items
        if "task" in item.title.lower() and "validation" in item.title.lower()
    ]

    assert len(task_validation_items) >= 1
    item = task_validation_items[0]

    assert item.impact == "high"
    assert item.confidence in ["high", "medium"]
    assert item.category in ["quality", "automation"]

def test_deduplication_within_summary():
    """Duplicate mentions in same summary are deduplicated."""
    # Create test summary with intentional duplicates
    test_content = """
    ## Pain Points
    - Task system violations occurred 3 times

    ## Recommendations
    - Add task format validation to prevent violations

    ## Action Items
    - Implement task format validation pre-commit hook
    """

    # Both mentions of "task format validation" should deduplicate
    items = extract_from_test_content(test_content)

    validation_items = [i for i in items if "validation" in i.title.lower()]
    assert len(validation_items) == 1  # Deduplicated to one item
```

---

### 2.5 Dry-Run Validation (1 hour)

#### Validation Process

1. **Select 3 representative summaries:**
   - Simple (1 focus area, few action items): `2025-10-17-windsurf-initiative-completion.md`
   - Medium (3-5 focus areas): `2025-10-18-task-attribution-fix.md`
   - Complex (10+ sections, multiple themes): `2025-10-15-daily-summary.md`

2. **Manual ground truth creation:**
   - Read each summary manually
   - Extract expected action items (5-10 per summary)
   - Document expected category, impact, confidence

3. **Run extraction pipeline:**

   ```bash
   python scripts/extract_action_items.py \
       docs/archive/session-summaries/2025-10-17-windsurf-initiative-completion.md \
       > output/2025-10-17-extracted.yaml
   ```

4. **Compare results:**
   - Precision: How many extracted items are valid?
   - Recall: How many expected items were extracted?
   - Accuracy: Correct classification (category, impact, confidence)?

5. **Iterative refinement:**
   - If precision <85%: Add negative examples to prompt
   - If recall <85%: Adjust section filtering, expand prompts
   - If classification wrong: Clarify criteria in system prompt

#### Success Metrics

| Metric | Target | Action if Below Target |
|--------|--------|------------------------|
| Precision | ≥85% | Tighten prompts, add validation rules |
| Recall | ≥85% | Expand section coverage, reduce skip list |
| Category Accuracy | ≥90% | Clarify category definitions |
| Impact Accuracy | ≥80% | Provide more examples in prompt |
| Confidence Accuracy | ≥75% | Refine confidence criteria |

---

## Deliverables

1. ✅ **Pydantic Schema:** `ActionItem` class with full validation
2. ✅ **Extraction Script:** `scripts/extract_action_items.py` with CLI
3. ✅ **System Prompt:** Tuned for action item extraction
4. ✅ **Test Suite:** 10+ tests covering schema, extraction, deduplication
5. ✅ **Validation Report:** Dry-run results on 3 summaries with metrics
6. ✅ **Logged Extractions:** SQLite database with all extraction attempts

---

## Success Criteria

- [ ] Schema validates all expected field types
- [ ] Extraction script runs successfully on sample summaries
- [ ] Precision ≥85%, Recall ≥85% on validation set
- [ ] Category/Impact/Confidence accuracy ≥75%
- [ ] All extractions logged to SQLite for analysis
- [ ] YAML output is valid and human-readable

---

## Next Phase

**Phase 3:** Deduplication & Validation Strategy - Design cross-summary deduplication and initiative mapping algorithms.

---

**Phase 2 Status:** Ready to Start
**Estimated Duration:** 4-5 hours
**Dependencies:** Phase 1 complete ✅
