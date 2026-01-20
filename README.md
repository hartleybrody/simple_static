# Simple Static
Create a simple static website using python and jinja templates.

Simple Static has a few pieces:

1. A `build` command that renders jinja templates to an output directory
2. A `serve` command that runs a local server & watches for changes to rebuild the site
3. A config parser that reads an optional `config.yaml` file to specify settings & add global context variables
4. Support for collecting a series of templates as "posts" and gathering common information to render them in a list
5. A plugin system to run your python scripts after your site is built

That's it.

----

## Getting Started

Install via [pip](https://pypi.org/project/simple-static/)

    pip install simple_static

A basic file structure for your project looks like this, pretty typical for static sites

    site/           # directory with .html jinja templates and other static files
    _build/         # directory where the site gets built to
    config.yaml     # optional yaml file

The package has two simple commands you can run from inside the root of your website, which is the directory that contains the `site` and `_build` directories as well as the optional `config.yaml` file.

Neither command takes parameters, everything is controlled via the config.yaml file, as described below.

Run a one-time build of your website

    build

Run a local server that serves your site and also watches for changes to files to trigger a rebuild

    serve

By default, your site will be served at http://localhost:8383.

## The Basics

There's an `INPUT_DIR` (defaults to `site`) which points to the folder that contains your jinja templates, as well as other static files (css, javascript, etc). There's also an `OUTPUT_DIR` (defaults to `_build`) that gets written to every time the site is rebuilt.

🧹 Don't edit any of the files in the `OUTPUT_DIR` directly as these are overwritten every time the site is rebuilt.

When setting up your static website:

- you can use any directory structure you like inside `INPUT_DIR`
- jinja templates should end in `.html`
- all other files in your site will be copied to `OUTPUT_DIR` as-is
- [see below](#posts) for how to setup a collection of posts

You can use all of the jinja features you expect like [base templates and inheritance](https://jinja.palletsprojects.com/en/3.0.x/templates/#template-inheritance). If you've never worked with jinja before, check out their helpful [Template Designer Documentation](https://jinja.palletsprojects.com/en/3.0.x/templates/) to learn the basics.

Template file names like `about.html` will be built to a file like `about/index.html` so that your site can have "pretty URLs" (ie `/about/`).

When jinja renders a template, we provide a "context" which is a set of variables that can be accessed in that  template file. The two ways to add things to the global site context are via [config](#config) and [posts](#posts).

## Config

Having a `config.yaml` at the outer level of your project is optional, but it allows you to both configure the site and also add global context variables you can use in your jinja templates.

Here's an example file that specifies the default site configuration values, and also adds a context variable:

```yaml
INPUT_DIR: "site"
OUTPUT_DIR: "_build"
LOCAL_HOST: "localhost"
LOCAL_PORT: 8383
SORT_POSTS_BY: created_at
PRETTY_URL: True

NAV_PAGES:
  - name: About
    url: /about/

  - name: Projects
    url: /projects/
```

You can add arbitrary keys to `config.yaml` and they will be added as context variables in all jinja templates. This is great for keeping track of site-wide things like nav menu items or the URL to your site's logo.

Note that the **key names are all lowercased before being passed to jinja**, so in the example above, you could render the nav items with `{% for nav_page in nav_pages %}...` in a jinja template.

If you make changes to your `config.yaml` file, you'll need to restart the `serve` command for them to be picked up, sorry about that.

## Posts
Posts are the basic unit for creating a feed of content. They could be anything -- employee pages, case studies of client work or simply blog entries. A post is no different than a regular page on the site, the main reason to use posts is if you'll want to render some sort of list or archive page that shows a quick snippet of each post on one page.

The posts feature allows you to extract some common metadata from each of the post templates in a collection (via their [block names in the jinja templates](https://jinja.palletsprojects.com/en/3.0.x/templates/#child-template)), and add that to the global site context.

In order to treat a collection of templates as a "series of posts" you simply put them in a directory (for example, `projects`) and add an empty file called `.posts` to that directory. That's it!

When the site is built, each of the templates inside that directory will get converted to a dict of `block_name`: `block_content`, and then added to a list. This list is sorted by the value inside the block named by `SORT_POSTS_BY` (which defaults to "created_at"), and the list gets added to the global site context, as the name of the directory (ie `projects`). Each post also automatically gets a `url` key that can be used for building links to that page on your site.

Here's an example:

    site/
        base.html
        index.html
        projects/
            .posts  # this file is empty, but triggers the "posts" collection
            foo.html
            bar.html

Here's what might be in `projects/foo.html`

    {% extends "base.html" %}

    {% block title %}Foo Project{% endblock %}
    {% block created_at %}1970-01-01{% endblock %}
    {% block desc %}
        Here is a quick blub that describes the first post ever!
    {% endblock %}

    {% block content %}
        Here is the content of the post that may be much longer.
    {% endblock %}

Note that each of those blocks inside the template are completely optional. The only one with any signifigance is `created_at` since it's the default name of the block used to sort the posts, but that can be changed in your `config.yaml` by changing the value of `SORT_POSTS_BY`.

Then, inside your `index.html` template file (or any other template file), you could have a snippet like this, which would print out the `title` and `desc` block for each of the posts, with a handy link to it.

    {% for project in projects %}
        <h2>
            {{project.title}}
        </h2>
        <p>
            {{project.desc}}
        </p>
        <a href="{{project.url}}">
            Read more...
        </a>
    {% endfor %}

Here, you see that you have access to a context variable called "projects" since that's the name of the directory that contains the `.post` file. The name for each of the attributes of a post ("title", "desc", etc) is totally up to you, and is taken from the name of the jinja block in the template file for that post. Try to make sure that all of the posts in a collection have the same named blocks, so you can print things correctly when looping through them.

## Plugins
Plugins are a simple system where we ...

## Contributing
This is my first time publishing a python project to PyPi, and I'd love to hear from you if you use it.

Feel free to [open an issue](https://github.com/hartleybrody/simple_static/issues/new) if you need any help or submit a PR if you want to fix anything or add features.

You can also [tweet me a link](https://twitter.com/hartbro/) if you use this to build a website! I may even add a link to your site here as well 🔗

## Publishing
Since I modify and publish this so infrequently, I'm adding instructions for myself on how to do it.

Update the package version in `setup.py`

Build the distribution packages:

```
python setup.py sdist bdist_wheel
```

Upload to PyPI (you'll be prompted for your PyPI credentials)
 - Set your username to `__token__`
 - Set your password to the token value, including the pypi- prefix, stored in .env file

```
twine upload dist/*
```
