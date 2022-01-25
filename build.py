from jinja2 import Environment, FileSystemLoader, select_autoescape

def build():

    env = Environment(
        loader=FileSystemLoader("site"),
        autoescape=select_autoescape()
    )

    template = env.get_template("page.html")
    print(template.render(the="variables", go="here"))

if __name__ == '__main__':
    build()