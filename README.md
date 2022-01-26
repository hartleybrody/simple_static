# Simple Static
Create a simple static website using python and jinja templates.

Simple Static has three pieces:

1. A `build` command that renders jinja templates to an `OUTPUT_DIR`
2. A `serve` command that runs a local server & watches for changes to rebuild the site
3. A config parses that reads an optional `config.yaml` file to specify settings & add context variables

That's it.

----

## Getting Started

Install

Usage

## The basics

There's an `INPUT_DIR` that contains your jinja templates, as well as other static files (css, javascript, etc). The default value is "site".

There's an `OUTPUT_DIR` that gets written to every time the site is rebuilt. The default value is "\_build". Don't edit any of the files in the `OUTPUT_DIR` directly as these are overwritten every time the site is rebuilt.

When setting up your static website:

- You can use any directory structure you like inside `INPUT_DIR`
- Jinja templates should end in `.html`
- All other files in your site will be copied to `OUTPUT_DIR` as-is

Note: Jinja templates file names like `about.html` will be rendered to `about/index.html` so that your site can have "pretty URLs" (ie `/about/`).

When developing your static website

- The static site serves on `http://localhost:8383` by default, you can set a different `LOCAL_PORT` in `config.yaml`
- You can add arbitrary keys to `config.yaml` and they will be added as context variables in all jinja templates
- If you make changes to your `config.yaml` file, you'll need to restart the `serve` command for them to be picked up