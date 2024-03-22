# Markdown->HTML static site generator

- Takes basic markdown files and converts to html
- Copies static assets to be used
- Project idea to implement something like Hugo
- Implemented own version of python filesystem utils: `os.walk`, `shutil.rmtree`, `shutil.copytree` - found in `src.utils`
- Generated code in `public/` directory

## Installation

- download the repo
- add a new venv
  - `python -m venv venv`
- activate it
  - `source venv/bin/activate`
- install local modules (no external dependencies)
  - dev: `pip install -e .`
  - prod: `pip install .`
- to deactivate venv: `deactivate`

## Usage

- All static files (images, styles etc.) to be put in `static/`
- All markdown files to be put in `content/`. Any non-markdown files will be ignored
- Currently `./template.html` defines page template
- To run the script: `./main.sh`
- To run the test suite: `./test.sh`

- Note after running the script with `./main.sh` we spin up a simple server to view the generated files
- Server on `http://localhost:8888`

## Improvements/Issues

- Markdown parsing is somewhat incomplete
- No support for nested inline formatting (e.g. bold and italic)
- No support for nested lists
- Have options for the page templates
