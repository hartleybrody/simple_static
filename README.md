# Simple Static
Create a simple static website using python and jinja templates.

Simple Static has three pieces:

1. A `build` command that renders jinja templates (ending in `.html`) and copies all other static files into an `OUTPUT_DIR` (`_build` by default)
2. A `serve` command that runs a local server (`http://localhost:8383` by default) and watches for changes to rebuild the site
3. A config parses that reads a `config.yaml` file to specify settings and add context variables to the jinja templates

That's it.