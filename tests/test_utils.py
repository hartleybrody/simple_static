import os

import sys
sys.path.append('.')
sys.path.append('tests')

from simple_static import utils as x
from simple_static.utils import config, TEMPLATE_SUFFIXES


class TestUtils:

    def test_is_template(self):
        assert x.is_template(os.path.join("foo.html"))
        assert x.is_template(os.path.join("foo", "bar.html"))

        assert x.is_template(os.path.join("base", "foo.html"))
        assert not x.is_template(os.path.join("base.html"))
        assert not x.is_template(os.path.join("base-foo.html"))

        assert not x.is_template(os.path.join("_foo", "bar.html"))
        assert not x.is_template(os.path.join("_foo.html"))

    def test_trim_input_dir(self):
        goal = os.path.join("foo", "bar")
        test = os.path.join(config.INPUT_DIR, "foo", "bar")
        assert x.trim_input_dir(test) == goal

        # paths get double nested sometimes, though they shouldn't...
        test = os.path.join(config.INPUT_DIR, config.INPUT_DIR, "foo", "bar")
        assert x.trim_input_dir(test) == goal

    def test_trim_output_dir(self):
        goal = os.path.join("foo", "bar")
        test = os.path.join(config.OUTPUT_DIR, "foo", "bar")
        assert x.trim_output_dir(test) == goal

        # paths get double nested sometimes, though they shouldn't...
        test = os.path.join(config.OUTPUT_DIR, config.OUTPUT_DIR, "foo", "bar")
        assert x.trim_output_dir(test) == goal

    def test_generate_output_path(self):
        cwd = os.getcwd()

        config.PRETTY_URL = True
        for suffix in TEMPLATE_SUFFIXES:
            goal = os.path.join(cwd, config.OUTPUT_DIR, "foo", "index.html")  # always .html ending
            assert x.generate_output_path(os.path.join(f"foo.{suffix}")) == goal
            assert x.generate_output_path(os.path.join(f"foo", f"index.{suffix}")) == goal

            goal = os.path.join(cwd, config.OUTPUT_DIR, "sitemap.xml")  # override prettification w flag
            assert x.generate_output_path(os.path.join(f"sitemap.xml"), can_prettify=False) == goal

        config.PRETTY_URL = False
        for suffix in TEMPLATE_SUFFIXES:
            pieces = [f"foo.{suffix}"]
            goal = os.path.join(cwd, config.OUTPUT_DIR, *pieces)
            assert x.generate_output_path(os.path.join(*pieces)) == goal

            pieces = ["foo", f"index.{suffix}"]
            goal = os.path.join(cwd, config.OUTPUT_DIR, *pieces)
            assert x.generate_output_path(os.path.join(*pieces)) == goal

        goal = os.path.join(config.OUTPUT_DIR, "sitemap.xml")  # don't add cwd when !full
        assert x.generate_output_path(os.path.join(f"sitemap.xml"), full=False) == goal

    def test_generate_output_url(self):
        goal = "/foo/"

        assert x.generate_output_url(os.path.join("foo")) == goal
        assert x.generate_output_url(os.path.join("foo", "index.html")) == goal
        assert x.generate_output_url(os.path.join(config.INPUT_DIR, "foo", "index.html")) == goal
        assert x.generate_output_url(os.path.join(config.OUTPUT_DIR, "foo", "index.html")) == goal


