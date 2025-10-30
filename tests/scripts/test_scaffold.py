from scripts.automation.scaffold import Scaffolder, TemplateType


def test_scaffolder_initialization() -> None:
    """Ensure scaffolding can locate initiative templates without raising errors."""

    scaffolder = Scaffolder(template_type=TemplateType.INITIATIVE_FLAT)
    template = scaffolder.jinja_env.get_template("initiative-flat.md.j2")

    assert template is not None
