"""Sphinx configuration."""

project = "Warehouse Ddd"
author = "Yarhushin Oleg"
copyright = "2024, Yarhushin Oleg"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
