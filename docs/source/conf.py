# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Добавляем корень проекта в sys.path, чтобы Sphinx нашёл модули
sys.path.insert(0, os.path.abspath('../..'))

project = 'PetHealth'
copyright = '2026, Макарова Варвара Николаевна'
author = 'Макарова Варвара Николаевна'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # автогенерация из docstrings
    'sphinx.ext.napoleon',     # поддержка Google/NumPy стиля docstrings
    'sphinx.ext.viewcode',     # ссылки на исходный код
    'sphinx.ext.autosummary',  # автоматические сводки
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'show-inheritance': True,
}

# Отключаем предупреждения о дубликатах в docstrings
suppress_warnings = ['duplicate_declaration']
