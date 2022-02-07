import os
import shutil
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .utils import get_template_paths, get_non_template_paths, config, logging

def build():

    env = Environment(
        loader=FileSystemLoader(config.INPUT_DIR),
        autoescape=select_autoescape()
    )

    try:
        shutil.rmtree(config.OUTPUT_DIR)  # nuke everything
    except FileNotFoundError:
        pass
    os.makedirs(config.OUTPUT_DIR)

    logging.info(f"building site from {os.sep}{config.INPUT_DIR}{os.sep} to {os.sep}{config.OUTPUT_DIR}{os.sep} at {datetime.now()}")

    # copy non-template static files (css, js, imgs, etc) into OUTPUT_DIR
    for path in get_non_template_paths():
        path = os.path.normpath(path)
        if not os.path.isfile(path):
            continue  # skip directories

        new_path = path.replace(config.INPUT_DIR, config.OUTPUT_DIR, 1)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        logging.info(f" copying {path} to {new_path}")
        shutil.copy(path, new_path)

    # render templates into OUTPUT_DIR
    for path in get_template_paths():
        path = os.path.normpath(path)

        f = path.split(f"{config.INPUT_DIR}{os.sep}")[1]
        template = env.get_template(f)

        output_path = generate_render_output_path(f)
        if not output_path:
            continue

        logging.info(f" {f:<20}\t==> {output_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # https://stackoverflow.com/a/12517490/625840
        with open(output_path, "w+") as f:

            html = template.render(**ctx)
            f.write(html)

def generate_render_output_path(f):
    pieces = f.split(os.sep)
    pieces[-1] = pieces[-1].replace(".html", "")  # strip file extension
    if pieces[-1].startswith("base"):
        return False  # 'base-*' prefix isn't a page
    if pieces[-1].startswith("_"):
        return False  # '_*' are layouts and not their own pages
    if pieces[-1].startswith("index"):
        pieces.pop()
    return os.path.join(os.getcwd(), config.OUTPUT_DIR, *pieces, "index.html")


if __name__ == '__main__':
    build()