import os
from glob import glob

# import these so we can expose them to plugins
from .utils import config, ctx, logging
from .utils import generate_output_path, trim_output_dir, generate_output_url

from jinja2 import Environment, FileSystemLoader, select_autoescape


def build_page(template_path, output_path, **user_context):
    """
    Useful for plugins that want to generate extra pages. Args:
        - template_path = file path to jinja template inside INPUT_DIR
        - output_path = desired place where file will live in OUTPUT_DIR
        - user_context = any other key/values to add to site context
    """

    for k, v in user_context.items():
        ctx[k] = v

    env = Environment(
        loader=FileSystemLoader(config.INPUT_DIR),
        autoescape=select_autoescape()
    )

    template = env.get_template(template_path)

    output_path = generate_output_path(output_path, can_prettify=False)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # https://stackoverflow.com/a/12517490/625840

    with open(output_path, "w+") as f:
        html = template.render(**ctx)
        f.write(html)


def get_pages():
    rendered_pages = glob(f"{config.OUTPUT_DIR}/**/*.html", recursive=True)
    return [{
        "file_path": page,
        "url_path": trim_output_dir(page),
        "pretty_url": generate_output_url(page),
    } for page in sorted(rendered_pages)]
