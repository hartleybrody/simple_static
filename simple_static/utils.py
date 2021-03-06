import os
import logging
from glob import glob

import yaml

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
    "SORT_POSTS_BY": "created_at",
    "PRETTY_URL": True,
    "LOG_LEVEL": "INFO",
    "PLUGINS": [],
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

# setup logging
logging.basicConfig(level=getattr(logging, config.LOG_LEVEL.upper()), format='%(message)s')

# view config to debug
[logging.debug(f"{k}: {getattr(config, k)}") for k in config.__dict__]

# move config values to context
ctx = {k.lower(): v for k, v in config.__dict__.items()}

TEMPLATE_SUFFIXES = ["html", "htm"]

def is_template(path):
    pieces = path.split(os.sep)
    if pieces[-1].startswith("base"):
        return False  # 'base-*' prefix isn't a page
    if pieces[-1].startswith("_"):
        return False  # '_*' are layouts and not their own pages
    if any([piece.startswith("_") for piece in pieces]):
        return False  # skip any directories with _* prefix
    return True

def trim_input_dir(path):
    pieces = path.split(os.sep)
    pieces = [p for p in pieces if p != config.INPUT_DIR]
    return os.path.join(*pieces)

def trim_output_dir(path):
    pieces = path.split(os.sep)
    pieces = [p for p in pieces if p != config.OUTPUT_DIR]
    return os.path.join(*pieces)

def generate_output_path(path, full=True, can_prettify=True):
    pieces = path.split(os.sep)

    if config.PRETTY_URL and can_prettify:
        for suffix in TEMPLATE_SUFFIXES:
            pieces[-1] = pieces[-1].replace(f".{suffix}", "")  # strip file extension
        if pieces[-1].startswith("index"):
            pieces.pop()  # don't double nest index documents
        final_pieces = [config.OUTPUT_DIR, *pieces, "index.html"]
    else:
        final_pieces = [config.OUTPUT_DIR, *pieces]
    if full:
        final_pieces.insert(0, os.getcwd())

    return os.path.join(*final_pieces)

def generate_output_url(path):
    # generate the URL that someone would visit in their browser, used with posts
    path = generate_output_path(path, full=False)
    trim = trim_output_dir(path)
    trim = trim_input_dir(trim)
    trim = trim.split("index.html")[0]
    if not trim.startswith("/"):
        trim = f"/{trim}"
    if not trim.endswith("/"):
        trim = f"{trim}/"
    return trim

def get_paths():
    return glob(f"{config.INPUT_DIR}/**/*.*", recursive=True)

def get_template_paths():
    paths = []
    for suffix in TEMPLATE_SUFFIXES:
        paths += glob(f"{config.INPUT_DIR}/**/*.{suffix}", recursive=True)
    return paths

def get_non_template_paths():
    to_return = []
    for path in glob(f"{config.INPUT_DIR}/**/*", recursive=True):
        if any([path.endswith(suffix) for suffix in TEMPLATE_SUFFIXES]):
            continue
        to_return.append(path)
    return to_return

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