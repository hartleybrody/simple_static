import os
import logging
from glob import glob

import yaml

# setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# setup config
try:
    with open("config.yaml", "r") as f:
        user_config = yaml.safe_load(f) or {}  # if file is blank, change from None to empty dict
except FileNotFoundError:
    user_config = {}

defaults = {
    "INPUT_DIR": "site",
    "OUTPUT_DIR": "_build",
    "LOCAL_HOST": "localhost",
    "LOCAL_PORT": "8383",
}

class Config(object):
    pass
config = Config()

# add user's properties
for k, v in user_config.items():
    setattr(config, k, v)

# add default properties
for k, v in defaults.items():
    if k not in dir(config):
        setattr(config, k, v)

# view config to debug
[logging.info(f"{k}: {getattr(config, k)}") for k in config.__dict__]

# move config values to context
ctx = {k.lower(): v for k, v in config.__dict__.items()}

def trim_input_dir(path):
    return path.split(f"{config.INPUT_DIR}{os.sep}")[1]

def get_paths():
    return glob(f"{config.INPUT_DIR}/**/*.*", recursive=True)

def get_template_paths():
    return glob(f"{config.INPUT_DIR}/**/*.html", recursive=True)

def get_non_template_paths():
    return glob(f"{config.INPUT_DIR}/**/*[!.html]", recursive=True)

def get_posts_dir():
    dot_posts_files = glob(f"{config.INPUT_DIR}/**/.posts", recursive=True)

    to_return = dict()
    for dot_post_file in dot_posts_files:
        key = dot_post_file.split(".posts")[0]
        posts = glob(f"{key}/*.html")
        for post in posts:
            if post.endswith("index.html"):  # index isn't a post
                posts.remove(post)
        to_return[key] = posts

    return to_return