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
        # print(template.render(the="variables", go="here"))

if __name__ == '__main__':
    build()