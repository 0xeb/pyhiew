"""Generate pydoc documentation for hiew module."""
import importlib
import sys

import hiew

sys.argv = ["pydoc", "-w", "hiew"]
module = importlib.import_module("pydoc")
module.cli()

hiew.Message("Done", "Documentation generated")
