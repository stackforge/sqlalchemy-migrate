#!/usr/bin/env python
# -*- coding: utf-8 -*-

import testtools


def main(imports=None):
    if imports:
        global suite
        suite = suite(imports)  # noqa
        defaultTest = 'fixture.suite'
    else:
        defaultTest = None
    return testtools.TestProgram(defaultTest=defaultTest)

from base import Base                               # noqa
from migrate.tests.fixture.pathed import Pathed     # noqa
from shell import Shell                             # noqa
from database import DB, usedb                      # noqa
