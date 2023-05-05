import os
import sys

import mock
import pytest

sys.path.append(".")
import <module-name>


class TestModule:
    def setup_method(self, _):
        """This setup method is optional and will run before every test.
        Good for things class instantiation or setting variables
        that will be reused in multiple tests.
        """

    def test_function(self):
        pass
