from glob import glob

import yaml

with open("conf.yaml", "r") as f:
    user_config = yaml.safe_load(f)
if not user_config:
    user_config = {}  # if file is blank, change from None to empty dict

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

# print config to debug
[print(f"{k}: {getattr(config, k)}") for k in dir(config) if not k.startswith("__")]

def get_template_paths():
    return glob(f"{config.INPUT_DIR}/**/*.html", recursive=True)