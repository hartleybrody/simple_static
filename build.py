import os
from glob import glob

from jinja2 import Environment, FileSystemLoader, select_autoescape

def build():

    env = Environment(
        loader=FileSystemLoader("site"),
        autoescape=select_autoescape()
    )

    for f in glob("site/**/*.html", recursive=True):
        f = f.split("site/")[1]
        template = env.get_template(f)
        print(f"======= {f} =======")

        output_path = generate_render_output_path(f)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # https://stackoverflow.com/a/12517490/625840

        with open(output_path, "w+") as f:
            html = template.render(the="variables", go="here")
            f.write(html)

def generate_render_output_path(f):
    pieces = f.split("/")
    pieces[-1] = pieces[-1].replace(".html", "")  # strip file extension
    return os.path.join(os.getcwd(), "_build/", *pieces, "index.html")


if __name__ == '__main__':
    build()