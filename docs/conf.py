# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

from augmenty.about import __version__

# -- Project information -----------------------------------------------------

project = "augmenty"
author = "Kenneth Enevoldsen"
github_user = "KenethEnevoldsen"
repo_url = f"https://github.com/{github_user}/{project}"


# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinxext.opengraph",
    "sphinx_copybutton",
    "sphinx.ext.githubpages",
    "myst_nb",
    "IPython.sphinxext.ipython_console_highlighting",
    "sphinx_design",
]

# autodoc_mock_imports = ["dacy"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "furo"  # "press", "sphinx_rtd_theme", "furo"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_show_sourcelink = True

html_context = {
    "display_github": True,  # Add 'Edit on Github' link instead of 'View page source'
    "github_user": "KennethEnevoldsen",
    "github_repo": project,
    "github_version": "main",
    "conf_py_path": "/docs/",
}


source_suffix = {
    ".rst": "restructuredtext",
    ".md": "myst-nb",
    ".ipynb": "myst-nb",
}
html_static_path = ["_static"]
html_favicon = "_static/favicon.ico"

html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": repo_url,
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,  # noqa: E501
            "class": "",
        },
    ],
    "source_repository": repo_url,
    "source_branch": "main",
    "source_directory": "docs/",
    "light_logo": "icon.png",
    "dark_logo": "icon_dark.png",
    "light_css_variables": {
        "color-brand-primary": "#ff5454",
        "color-brand-content": "#ff7575",
    },
    "dark_css_variables": {
        "color-brand-primary": "#ff8f8f",
        "color-brand-content": "#ff8f8f",
    },
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
}

# pygments_style = "monokai"
# pygments_dark_style = "monokai"
