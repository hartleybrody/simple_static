import logging
from glob import glob

import yaml

# setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# setup config
with open("conf.yaml", "r") as f:
    user_config = yaml.safe_load(f) or {}  # if file is blank, change from None to empty dict

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

def get_template_paths():
    return glob(f"{config.INPUT_DIR}/**/*.html", recursive=True)

def get_non_template_paths():
    return glob(f"{config.INPUT_DIR}/**/*[!.html]", recursive=True)