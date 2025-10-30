from pathlib import Path
import pytest
from scripts.automation.scaffold import Scaffolder, TemplateType

def test_scaffolder_initialization():
    """
    Tests that the Scaffolder class can be initialized and finds its templates.
    This is a regression test for the template path bug.
    """
    try:
        scaffolder = Scaffolder(template_type=TemplateType.INITIATIVE_FLAT)
        # The real test is that this doesn't raise a TemplateNotFound error
        assert scaffolder.jinja_env.get_template("initiative-flat.md.j2")
    except Exception as e:
        pytest.fail(f"Scaffolder initialization failed: {e}")
