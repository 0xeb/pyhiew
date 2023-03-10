import importlib
import sys

import hiew

module_name = "pydoc"  # Replace with the name of your module
args = ["-w", "hiew"]  # Replace with any command-line arguments
sys.argv = [module_name] + args  # Set the command-line arguments

module = importlib.import_module(module_name)

module.cli()  # Call the main function in the module
hiew.MessageBox("pause", "Pause")