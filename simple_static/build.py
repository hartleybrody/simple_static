import os
import shutil
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .utils import *
from .utils import config, logging, ctx

def build():

    for plugin in config.PRE_PLUGINS:
        logging.info(f"running pre-plugin: {plugin}")
        exec(open(plugin).read())

    env = Environment(
        loader=FileSystemLoader(config.INPUT_DIR),
        autoescape=select_autoescape()
    )

    try:
        shutil.rmtree(config.OUTPUT_DIR)  # nuke everything
    except FileNotFoundError:
        pass
    os.makedirs(config.OUTPUT_DIR)

    t0 = datetime.now()
    logging.info(f"building site from {os.sep}{config.INPUT_DIR}{os.sep} to {os.sep}{config.OUTPUT_DIR}{os.sep} at {t0}")

    # copy non-template static files (css, js, imgs, etc) into OUTPUT_DIR
    for path in get_non_template_paths():
        path = os.path.normpath(path)
        if not os.path.isfile(path):
            continue  # skip directories

        new_path = path.replace(config.INPUT_DIR, config.OUTPUT_DIR, 1)
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        logging.debug(f" copying {path} to {new_path}")
        shutil.copy(path, new_path)

    # load .posts directory data into context
    for post_dir, posts in get_posts_dir().items():
        logging.info(f"{post_dir} directory has {len(posts)} posts")
        key = trim_input_dir(post_dir).replace(os.sep, "")

        if key.lower() in ctx:
            logging.warning(f"!! overwriting existing '{key}' in context with {post_dir} content")
        ctx[key] = []

        for path in posts:
            logging.debug(f"  {path} is a post")
            f = trim_input_dir(path)
            template = env.get_template(f)
            post = dict(url=generate_output_url(f))
            for block_title, block_content in template.blocks.items():
                post[block_title] = "".join(block_content(template.new_context())).strip()
            ctx[key].append(post)

        ctx[key] = sorted(ctx[key], key=lambda x: x.get(config.SORT_POSTS_BY, ""), reverse=True)

    # render templates into OUTPUT_DIR
    for path in get_template_paths():
        path = os.path.normpath(path)
        if not is_template(path):
            continue

        f = trim_input_dir(path)
        template = env.get_template(f)

        output_path = generate_output_path(f)

        logging.debug(f" {f:<20}\t==> {output_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # https://stackoverflow.com/a/12517490/625840
        with open(output_path, "w+") as f:

            html = template.render(**ctx)
            f.write(html)

    for plugin in config.PLUGINS:
        logging.info(f"running plugin: {plugin}")
        exec(open(plugin).read())

    t1 = datetime.now()
    logging.debug(f"finished building at {t1}, took {t1 - t0}")


if __name__ == '__main__':
    build()