# Simple Static
Create a simple static website using python and jinja templates.

Simple Static has three pieces:

1. A `build` command that renders jinja templates to an `OUTPUT_DIR`
2. A `serve` command that runs a local server & watches for changes to rebuild the site
3. A config parser that reads an optional `config.yaml` file to specify settings & add context variables

That's it.

----

## Getting Started

Install

Usage

## The basics

There's an `INPUT_DIR` that contains your jinja templates, as well as other static files (css, javascript, etc). The default value is "site". There's an `OUTPUT_DIR` that gets written to every time the site is rebuilt. The default value is "\_build". Don't edit any of the files in the `OUTPUT_DIR` directly as these are overwritten every time the site is rebuilt.

When setting up your static website:

- You can use any directory structure you like inside `INPUT_DIR`
- Jinja templates should end in `.html`
- All other files in your site will be copied to `OUTPUT_DIR` as-is

You can use all of the jinja features you expect like [base templates and inheritance](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance).

Note: Jinja templates file names like `about.html` will be rendered to `about/index.html` so that your site can have "pretty URLs" (ie `/about/`).

## Config

Note that having a `config.yaml` inside of your `INPUT_DIR` is optional, but allows you to configure the site and add context variables. Here's an example file that specifies the default vaules:

```yaml
INPUT_DIR: "site"
OUTPUT_DIR: "_build"
LOCAL_HOST: "localhost"
LOCAL_PORT: 8383

arbitrary_key: arbitrary_value
```

You can add arbitrary keys to `config.yaml` and they will be added as context variables in all jinja templates. Note that the **key names are all lowercased before being passed to jinja**, so you could specify `MY_VAR: foo` in your config and then render it with `{{ my_var }}` in a jinja template.

If you make changes to your `config.yaml` file, you'll need to restart the `serve` command for them to be picked up.