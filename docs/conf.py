"""Sphinx configuration."""

project = "Desk Python SDK"
author = "chenciao8"
copyright = "2025, chenciao8"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
