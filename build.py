import os
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

from utils import get_template_paths, INPUT_PREFIX, OUTPUT_PREFIX

def build():

    env = Environment(
        loader=FileSystemLoader(INPUT_PREFIX),
        autoescape=select_autoescape()
    )

    try:
        shutil.rmtree(OUTPUT_PREFIX)  # nuke everything
    except FileNotFoundError:
        pass
    os.makedirs(OUTPUT_PREFIX)

    print(f"building site from {os.sep}{INPUT_PREFIX}{os.sep} to {os.sep}{OUTPUT_PREFIX}{os.sep}")

    for path in get_template_paths():
        path = os.path.normpath(path)

        f = path.split(f"{INPUT_PREFIX}{os.sep}")[1]
        template = env.get_template(f)

        output_path = generate_render_output_path(f)
        if not output_path:
            continue

        print(f" {f:<20}\t==> {output_path}")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # https://stackoverflow.com/a/12517490/625840
        with open(output_path, "w+") as f:
            html = template.render(the="variables", go="here")
            f.write(html)

def generate_render_output_path(f):
    pieces = f.split(os.sep)
    pieces[-1] = pieces[-1].replace(".html", "")  # strip file extension
    if pieces[-1].startswith("base"):
        return False
    return os.path.join(os.getcwd(), OUTPUT_PREFIX, *pieces, "index.html")


if __name__ == '__main__':
    build()