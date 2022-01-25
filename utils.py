from glob import glob

INPUT_PREFIX = "site"
OUTPUT_PREFIX = "_build"

def get_template_paths():
	return glob(f"{INPUT_PREFIX}/**/*.html", recursive=True)