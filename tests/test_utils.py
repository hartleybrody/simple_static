import os

import sys
sys.path.append('.')
sys.path.append('tests')

from simple_static import utils as x
from simple_static.utils import config


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
