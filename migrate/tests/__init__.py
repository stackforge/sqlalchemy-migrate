# make this package available during imports as long as we support <python2.5
import os
import sys
from unittest import TestCase
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import migrate
import six


class TestVersionDefined(TestCase):
    def test_version(self):
        """Test for migrate.__version__"""
        self.assertTrue(isinstance(migrate.__version__, six.string_types))
        self.assertTrue(len(migrate.__version__) > 0)
