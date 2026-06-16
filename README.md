# nomad-plugin-tutorials

This repo contains tutorials for learning how to develop NOMAD plugin entry
points. We recommend using it in conjunction with the
[Tutorial documentation on plugin development](https://fairmat-nfdi.github.io/nomad-docs/tutorial/develop_plugin/plugin_structure.html
).

## Getting Started

To go through the tutorials in this repo, start with cloning it on your local:

```sh
git clone git@github.com:FAIRmat-NFDI/nomad-plugin-tutorials.git
cd nomad-plugin-tutorials
```

Next step, install the package in editable mode along with its development
dependencies in a virtual Python environment (Python>=3.10).

Installation with [uv](https://docs.astral.sh/uv/) (recommended):
```sh
uv sync --extra dev
. .venv/bin/activate
```

If you don't use uv, install with pip instead:
```sh
python3.12 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -e '.[dev]'
```

## Tutorial mode

Some tutorials offer code-along exercises where the user needs to implement
missing code snippets. To access this _"tutorial mode"_ version of code, switch
to the `tutorial-mode` branch. The `main` branch has fully operational code
that can be used as ground truth for these exercises. Use git-checkout to switch
branches:

```sh
git checkout tutorial-mode  # to switch to tutorial-mode branch
```

## Directory structure

```sh
src
└── nomad_plugin_tutorials
    ├── schema                # Tutorial for Schema entry point
    │   ├── __init__.py
    │   ├── schema_package.py
    │   ├── tutorial.ipynb
    │   ├── calculate.py
    │   └── visualize.py
    └── parsers               # Three tutorials for Parser entry point
        ├── tutorial_1/       # - Use Matching Parser to create a non-editable entry
        ├── tutorial_2/       # - Manually create an editable entry that parses data file
        ├── tutorial_3/       # - Use Matching Parser to create an editable entry that parses data file
        ├── reader.py
        ├── utils.py
        └── data/             # Example data files for parsing
```

## Switching entry points for Parser tutorials

When using the repo in _"tutorial mode"_, you might need to test if your code
snippets are working as expected. To test the code, the corresponding plugin
entry point should be made available in the environment through
`pyproject.toml`.

By default the entry point for schema tutorial and parser tutorial 1 are
available. When working on one of the parser tutorials, add the corresponding entry point while commenting out others in `pyproject.toml`. For example, here's how `pyproject.toml` should look like when working with parser tutorial 3:

```toml
# pyproject.toml

[project.entry-points.'nomad.plugin']
# parser_tutorial_1_schema = "nomad_plugin_tutorials.parsers.tutorial_1.schema:microscopy"
# parser_tutorial_1_parser = "nomad_plugin_tutorials.parsers.tutorial_1.parsers:microscopy"

# parser_tutorial_2_schema = "nomad_plugin_tutorials.parsers.tutorial_2.schema:microscopy"

parser_tutorial_3_schema = "nomad_plugin_tutorials.parsers.tutorial_3.schema:microscopy"
parser_tutorial_3_parser = "nomad_plugin_tutorials.parsers.tutorial_3.parsers:microscopy"
...
```

## Main contributors

| Name | E-mail     |
|------|------------|
| Lev Ginzburg | [lev.ginzburg@physik.hu-berlin.de](mailto:lev.ginzburg@physik.hu-berlin.de)
| Sarthak Kapoor | [sarthak.kapoor@physik.hu-berlin.de](mailto:sarthak.kapoor@physik.hu-berlin.de)
