#!/usr/bin/env python3
"""Template scaffolding tool for mcp-web project.

Usage:
    python scripts/scaffold.py --type initiative
    python scripts/scaffold.py --type adr --config config.yaml --dry-run
    task scaffold:initiative
"""

import json
import re
import subprocess
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any

import click
import jinja2
import yaml


class TemplateType(str, Enum):
    """Supported template types."""

    INITIATIVE_FLAT = "initiative"
    INITIATIVE_FOLDER = "initiative-folder"
    ADR = "adr"
    SESSION_SUMMARY = "summary"


class ScaffoldMode(str, Enum):
    """Scaffolding modes."""

    INTERACTIVE = "interactive"  # Prompt user for fields
    CONFIG = "config"  # Load from YAML/JSON config
    MINIMAL = "minimal"  # Use defaults, prompt only required


@click.command()
@click.option(
    "--type",
    "template_type",
    type=click.Choice([t.value for t in TemplateType]),
    required=True,
    help="Type of template to scaffold",
)
@click.option(
    "--mode",
    type=click.Choice([m.value for m in ScaffoldMode]),
    default="interactive",
    help="Scaffolding mode",
)
@click.option(
    "--config",
    type=click.Path(exists=True),
    help="Config file (YAML/JSON) for non-interactive mode",
)
@click.option("--output", type=click.Path(), help="Output path (default: auto-generate)")
@click.option("--dry-run", is_flag=True, help="Show output without writing")
@click.option("--validate-only", is_flag=True, help="Validate template without rendering")
def scaffold(
    template_type: str,
    mode: str,
    config: str | None,
    output: str | None,
    dry_run: bool,
    validate_only: bool,
) -> None:
    """Scaffold a new document from template."""
    scaffolder = Scaffolder(template_type=TemplateType(template_type))

    if validate_only:
        scaffolder.validate_template()
        click.echo("✓ Template valid")
        return

    # Auto-detect mode from config file if not explicitly set
    if config and mode == "interactive":
        mode = "config"

    # Gather fields
    if mode == "interactive":
        fields = scaffolder.prompt_interactive()
    elif mode == "config" and config:
        fields = scaffolder.load_config(config)
    else:
        fields = scaffolder.use_defaults()

    # Render template
    content = scaffolder.render(fields)

    # Determine output path
    output_path = Path(output) if output else scaffolder.generate_path(fields)

    if dry_run:
        click.echo(f"Would write to: {output_path}")
        click.echo("=" * 80)
        click.echo(content)
        return

    # Write file
    scaffolder.write_file(output_path, content)

    # Validate generated file
    if not scaffolder.validate_output(output_path):
        click.echo("⚠️  Warning: Generated file has validation issues", err=True)
        return

    click.echo(f"✓ Created: {output_path}")


class Scaffolder:
    """Template scaffolding engine."""

    def __init__(self, template_type: TemplateType):
        self.template_type = template_type
        self.template_dir = Path(__file__).parent / "templates"
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def prompt_interactive(self) -> dict[str, Any]:
        """Prompt user for template fields."""
        schema = self.get_schema()
        fields = {}

        click.echo(f"\n=== Creating {self.template_type.value} ===\n")

        for field_name, field_def in schema.items():
            # Skip auto-generated fields
            if field_def.get("auto"):
                fields[field_name] = field_def["default"]
                continue

            # Handle list fields
            if field_def.get("type") == "list":
                fields[field_name] = self._prompt_list(field_def)
                continue

            # Handle dict list fields
            if field_def.get("type") == "dict_list":
                fields[field_name] = self._prompt_dict_list(field_def)
                continue

            # Prompt user for simple fields
            prompt_text = field_def["label"]
            if field_def.get("required"):
                prompt_text += " (required)"
            if "default" in field_def:
                prompt_text += f" [{field_def['default']}]"

            if field_def.get("type") == "choice":
                value = click.prompt(
                    prompt_text,
                    type=click.Choice(field_def["choices"]),
                    default=field_def.get("default"),
                )
            elif field_def.get("type") == "bool":
                value = click.confirm(prompt_text, default=field_def.get("default", False))
            else:
                value = click.prompt(prompt_text, type=str, default=field_def.get("default", ""))

            fields[field_name] = value

        return fields

    def _prompt_list(self, field_def: dict[str, Any]) -> list[str]:
        """Prompt for list of items."""
        click.echo(f"\n{field_def['label']} (one per line, empty line to finish):")
        items = []
        while True:
            item = click.prompt("  ", default="", show_default=False)
            if not item:
                break
            items.append(item)
        return items if items else field_def.get("default", [])

    def _prompt_dict_list(self, field_def: dict[str, Any]) -> list[dict[str, Any]]:
        """Prompt for list of dictionaries."""
        click.echo(f"\n{field_def['label']}:")
        items = []

        if not click.confirm("  Add entry?", default=True):
            return field_def.get("default", [])

        while True:
            item = {}
            for subfield_name, subfield_def in field_def["schema"].items():
                value = click.prompt(f"    {subfield_def['label']}", type=str)
                item[subfield_name] = value

            items.append(item)

            if not click.confirm("  Add another entry?", default=False):
                break

        return items

    def get_schema(self) -> dict[str, dict[str, Any]]:
        """Get field schema for template type."""
        schemas = {
            TemplateType.INITIATIVE_FLAT: {
                "title": {
                    "label": "Initiative title",
                    "type": "str",
                    "required": True,
                },
                "owner": {"label": "Owner", "type": "str", "default": "@ai-agent"},
                "priority": {
                    "label": "Priority",
                    "type": "choice",
                    "choices": ["critical", "high", "medium", "low"],
                    "default": "medium",
                },
                "estimated_duration": {
                    "label": "Estimated duration",
                    "type": "str",
                    "default": "2-3 weeks",
                },
                "target_completion": {
                    "label": "Target completion (YYYY-MM-DD, optional)",
                    "type": "str",
                    "default": "",
                },
                "objective": {
                    "label": "Objective (1-2 sentences)",
                    "type": "str",
                    "required": True,
                },
                "problem": {
                    "label": "Problem being solved",
                    "type": "str",
                    "required": True,
                },
                "impact": {"label": "Impact/Why important", "type": "str", "required": True},
                "value": {"label": "Value/Benefit", "type": "str", "required": True},
                "success_criteria": {
                    "label": "Success criteria",
                    "type": "list",
                    "default": [],
                },
                "in_scope": {"label": "In scope items", "type": "list", "default": []},
                "out_of_scope": {
                    "label": "Out of scope items",
                    "type": "list",
                    "default": [],
                },
                "phases": {
                    "label": "Phases with tasks",
                    "type": "dict_list",
                    "schema": {
                        "name": {"label": "Phase name"},
                        "tasks": {"label": "Tasks (comma-separated)"},
                    },
                    "default": [],
                },
                "dependencies": {"label": "Dependencies", "type": "list", "default": []},
                "risks": {
                    "label": "Risks",
                    "type": "dict_list",
                    "schema": {
                        "description": {"label": "Risk description"},
                        "impact": {"label": "Impact (Low/Medium/High)"},
                        "likelihood": {"label": "Likelihood (Low/Medium/High)"},
                        "mitigation": {"label": "Mitigation strategy"},
                    },
                    "default": [],
                },
                "timeline": {
                    "label": "Timeline",
                    "type": "dict_list",
                    "schema": {
                        "period": {"label": "Period (e.g., Week 1-2)"},
                        "description": {"label": "Description"},
                    },
                    "default": [],
                },
                "related_docs": {
                    "label": "Related documentation",
                    "type": "dict_list",
                    "schema": {
                        "title": {"label": "Document title"},
                        "path": {"label": "Document path"},
                    },
                    "default": [],
                },
                "created": {
                    "label": "Created date",
                    "type": "str",
                    "auto": True,
                    "default": self.today(),
                },
                "status": {
                    "label": "Status",
                    "type": "str",
                    "auto": True,
                    "default": "Proposed",
                },
            },
            TemplateType.INITIATIVE_FOLDER: {
                # Same schema as INITIATIVE_FLAT - different output structure (folder vs file)
                "title": {
                    "label": "Initiative title",
                    "type": "str",
                    "required": True,
                },
                "owner": {"label": "Owner", "type": "str", "default": "@ai-agent"},
                "priority": {
                    "label": "Priority",
                    "type": "choice",
                    "choices": ["critical", "high", "medium", "low"],
                    "default": "medium",
                },
                "estimated_duration": {
                    "label": "Estimated duration",
                    "type": "str",
                    "default": "2-3 weeks",
                },
                "target_completion": {
                    "label": "Target completion (YYYY-MM-DD, optional)",
                    "type": "str",
                    "default": "",
                },
                "objective": {
                    "label": "Objective (1-2 sentences)",
                    "type": "str",
                    "required": True,
                },
                "problem": {
                    "label": "Problem being solved",
                    "type": "str",
                    "required": True,
                },
                "impact": {"label": "Impact/Why important", "type": "str", "required": True},
                "value": {"label": "Value/Benefit", "type": "str", "required": True},
                "success_criteria": {
                    "label": "Success criteria",
                    "type": "list",
                    "default": [],
                },
                "in_scope": {"label": "In scope items", "type": "list", "default": []},
                "out_of_scope": {
                    "label": "Out of scope items",
                    "type": "list",
                    "default": [],
                },
                "phases": {
                    "label": "Phases with tasks",
                    "type": "dict_list",
                    "schema": {
                        "name": {"label": "Phase name"},
                        "tasks": {"label": "Tasks (comma-separated)"},
                    },
                    "default": [],
                },
                "dependencies": {"label": "Dependencies", "type": "list", "default": []},
                "risks": {
                    "label": "Risks",
                    "type": "dict_list",
                    "schema": {
                        "description": {"label": "Risk description"},
                        "impact": {"label": "Impact (Low/Medium/High)"},
                        "likelihood": {"label": "Likelihood (Low/Medium/High)"},
                        "mitigation": {"label": "Mitigation strategy"},
                    },
                    "default": [],
                },
                "timeline": {
                    "label": "Timeline",
                    "type": "dict_list",
                    "schema": {
                        "period": {"label": "Period (e.g., Week 1-2)"},
                        "description": {"label": "Description"},
                    },
                    "default": [],
                },
                "related_docs": {
                    "label": "Related documentation",
                    "type": "dict_list",
                    "schema": {
                        "title": {"label": "Document title"},
                        "path": {"label": "Document path"},
                    },
                    "default": [],
                },
                "created": {
                    "label": "Created date",
                    "type": "str",
                    "auto": True,
                    "default": self.today(),
                },
                "status": {
                    "label": "Status",
                    "type": "str",
                    "auto": True,
                    "default": "Proposed",
                },
            },
            TemplateType.ADR: {
                "title": {"label": "Decision title", "type": "str", "required": True},
                "number": {
                    "label": "ADR number",
                    "type": "int",
                    "auto": True,
                    "default": self.next_adr_number(),
                },
                "status": {
                    "label": "Status",
                    "type": "choice",
                    "choices": ["proposed", "accepted", "rejected", "superseded"],
                    "default": "proposed",
                },
                "date": {
                    "label": "Date",
                    "type": "str",
                    "auto": True,
                    "default": self.today(),
                },
                "deciders": {
                    "label": "Deciders",
                    "type": "str",
                    "default": "Core team",
                },
                "tags": {"label": "Tags (comma-separated)", "type": "str", "default": ""},
                "context": {
                    "label": "Context (problem description)",
                    "type": "str",
                    "required": True,
                },
                "decision": {
                    "label": "Decision (what was decided)",
                    "type": "str",
                    "required": True,
                },
                "alternatives": {
                    "label": "Alternatives considered",
                    "type": "dict_list",
                    "schema": {
                        "name": {"label": "Alternative name"},
                        "description": {"label": "Description"},
                        "pros": {"label": "Pros (comma-separated)"},
                        "cons": {"label": "Cons (comma-separated)"},
                        "rejection_reason": {"label": "Reason for rejection"},
                    },
                    "default": [],
                },
                "positive_consequences": {
                    "label": "Positive consequences",
                    "type": "list",
                    "default": [],
                },
                "negative_consequences": {
                    "label": "Negative consequences",
                    "type": "list",
                    "default": [],
                },
                "neutral_consequences": {
                    "label": "Neutral consequences",
                    "type": "list",
                    "default": [],
                },
                "implementation": {
                    "label": "Implementation details",
                    "type": "str",
                    "default": "",
                },
                "references": {"label": "References", "type": "list", "default": []},
                "author": {
                    "label": "Author",
                    "type": "str",
                    "default": "Cascade",
                },
            },
            TemplateType.SESSION_SUMMARY: {
                "title": {"label": "Session title", "type": "str", "required": True},
                "date": {
                    "label": "Date",
                    "type": "str",
                    "auto": True,
                    "default": self.today(),
                },
                "duration": {"label": "Duration", "type": "str", "default": "~2 hours"},
                "session_type": {
                    "label": "Session type",
                    "type": "choice",
                    "choices": ["implementation", "planning", "research", "debugging"],
                    "default": "implementation",
                },
                "initiative": {
                    "label": "Related initiative",
                    "type": "str",
                    "default": "",
                },
                "objectives": {
                    "label": "Session objectives",
                    "type": "str",
                    "required": True,
                },
                "accomplishments": {
                    "label": "Accomplishments",
                    "type": "dict_list",
                    "schema": {
                        "action": {"label": "Action (e.g., Created, Fixed)"},
                        "description": {"label": "Description"},
                        "files": {"label": "Files (optional)"},
                    },
                    "default": [],
                },
                "decisions": {
                    "label": "Key decisions",
                    "type": "dict_list",
                    "schema": {
                        "topic": {"label": "Decision topic"},
                        "decision": {"label": "What was decided"},
                        "rationale": {"label": "Rationale"},
                    },
                    "default": [],
                },
                "learnings": {
                    "label": "Technical learnings",
                    "type": "dict_list",
                    "schema": {
                        "category": {"label": "Category/Technology"},
                        "insight": {"label": "What was learned"},
                    },
                    "default": [],
                },
                "issues": {
                    "label": "Unresolved issues",
                    "type": "dict_list",
                    "schema": {
                        "area": {"label": "Component/Area"},
                        "problem": {"label": "Problem description"},
                        "reason": {"label": "Why unresolved"},
                    },
                    "default": [],
                },
                "next_steps": {"label": "Next steps", "type": "list", "default": []},
                "metrics": {
                    "label": "Metrics",
                    "type": "dict_list",
                    "schema": {
                        "files_modified": {"label": "Files modified"},
                        "commits": {"label": "Commits"},
                        "tests_passing": {"label": "Tests passing"},
                        "tests_total": {"label": "Tests total"},
                        "adrs_created": {"label": "ADRs created (optional)"},
                        "duration_minutes": {"label": "Duration in minutes (optional)"},
                    },
                    "default": [],
                },
            },
        }
        return schemas[self.template_type]

    def load_config(self, config_path: str) -> dict[str, Any]:
        """Load configuration from YAML or JSON file."""
        config_file = Path(config_path)
        content = config_file.read_text()

        if config_file.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(content)
        elif config_file.suffix == ".json":
            return json.loads(content)
        else:
            raise ValueError(f"Unsupported config format: {config_file.suffix}")

    def use_defaults(self) -> dict[str, Any]:
        """Use default values for all fields."""
        schema = self.get_schema()
        fields = {}
        for field_name, field_def in schema.items():
            fields[field_name] = field_def.get("default", "")
        return fields

    def render(self, fields: dict[str, Any]) -> str:
        """Render template with fields."""
        # Preprocess fields
        fields = self._preprocess_fields(fields)

        # Map template types to template files
        template_files = {
            TemplateType.INITIATIVE_FLAT: "initiative-flat.md.j2",
            TemplateType.INITIATIVE_FOLDER: "initiative-flat.md.j2",  # Same template, different output structure
            TemplateType.ADR: "adr.md.j2",
            TemplateType.SESSION_SUMMARY: "session-summary.md.j2",
        }
        template_file = template_files[self.template_type]
        template = self.jinja_env.get_template(template_file)
        return template.render(**fields)

    def _preprocess_fields(self, fields: dict[str, Any]) -> dict[str, Any]:
        """Preprocess fields before rendering."""
        # Convert comma-separated strings to lists
        if (
            self.template_type == TemplateType.ADR
            and "tags" in fields
            and isinstance(fields["tags"], str)
        ):
            fields["tags"] = [t.strip() for t in fields["tags"].split(",") if t.strip()]

        # Process alternatives: split pros/cons
        if self.template_type == TemplateType.ADR and "alternatives" in fields:
            for alt in fields["alternatives"]:
                if "pros" in alt and isinstance(alt["pros"], str):
                    alt["pros"] = [p.strip() for p in alt["pros"].split(",") if p.strip()]
                if "cons" in alt and isinstance(alt["cons"], str):
                    alt["cons"] = [c.strip() for c in alt["cons"].split(",") if c.strip()]

        # Process phases: split tasks
        if self.template_type == TemplateType.INITIATIVE_FLAT and "phases" in fields:
            for phase in fields["phases"]:
                if "tasks" in phase and isinstance(phase["tasks"], str):
                    phase["tasks"] = [t.strip() for t in phase["tasks"].split(",") if t.strip()]

        return fields

    def generate_path(self, fields: dict[str, Any]) -> Path:
        """Generate output path from fields."""
        if self.template_type == TemplateType.INITIATIVE_FLAT:
            filename = self.slugify(fields["title"])
            # Use provided 'created' date or default to today
            created_date = fields.get("created", self.today())
            return Path("docs/initiatives/active") / f"{created_date}-{filename}.md"
        elif self.template_type == TemplateType.INITIATIVE_FOLDER:
            filename = self.slugify(fields["title"])
            created_date = fields.get("created", self.today())
            # Return path to initiative.md inside folder
            return Path("docs/initiatives/active") / f"{created_date}-{filename}" / "initiative.md"
        elif self.template_type == TemplateType.ADR:
            number = fields["number"]
            title = self.slugify(fields["title"])
            return Path("docs/adr") / f"{number:04d}-{title}.md"
        elif self.template_type == TemplateType.SESSION_SUMMARY:
            title = self.slugify(fields["title"])
            # Use provided 'date' field or default to today
            summary_date = fields.get("date", self.today())
            return Path("docs/archive/session-summaries") / f"{summary_date}-{title}.md"
        else:
            raise ValueError(f"Unknown template type: {self.template_type}")

    def write_file(self, path: Path, content: str) -> None:
        """Write content to file and create folder structure if needed."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

        # For folder-based initiatives, create artifacts/ and phases/ directories
        if self.template_type == TemplateType.INITIATIVE_FOLDER:
            initiative_dir = path.parent
            (initiative_dir / "artifacts").mkdir(exist_ok=True)
            (initiative_dir / "phases").mkdir(exist_ok=True)
            click.echo(f"✓ Created folder structure: {initiative_dir}/")
            click.echo("  - artifacts/")
            click.echo("  - phases/")

    def validate_template(self) -> bool:
        """Validate template can be loaded."""
        try:
            template_files = {
                TemplateType.INITIATIVE_FLAT: "initiative-flat.md.j2",
                TemplateType.INITIATIVE_FOLDER: "initiative-flat.md.j2",
                TemplateType.ADR: "adr.md.j2",
                TemplateType.SESSION_SUMMARY: "session-summary.md.j2",
            }
            template_file = template_files[self.template_type]
            self.jinja_env.get_template(template_file)
            return True
        except jinja2.TemplateError as e:
            click.echo(f"Template error: {e}", err=True)
            return False

    def validate_output(self, path: Path) -> bool:
        """Validate generated file."""
        # Run markdownlint
        try:
            result = subprocess.run(
                ["npx", "markdownlint-cli2", str(path)],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                click.echo(f"Markdown linting failed:\n{result.stdout}", err=True)
                return False
        except FileNotFoundError:
            click.echo("markdownlint-cli2 not found, skipping validation", err=True)
            return True

        return True

    @staticmethod
    def today() -> str:
        """Get today's date in YYYY-MM-DD format."""
        return date.today().isoformat()

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to kebab-case slug."""
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[\s_]+", "-", text)
        return text.strip("-")

    @staticmethod
    def next_adr_number() -> int:
        """Get next ADR number."""
        adr_dir = Path("docs/adr")
        if not adr_dir.exists():
            return 1

        existing = [f.stem.split("-")[0] for f in adr_dir.glob("*.md")]
        numbers = [int(n) for n in existing if n.isdigit()]
        return max(numbers, default=0) + 1


if __name__ == "__main__":
    scaffold()
