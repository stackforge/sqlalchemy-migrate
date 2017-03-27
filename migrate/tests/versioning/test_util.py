#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from sqlalchemy import *

from migrate.exceptions import MigrateDeprecationWarning
from migrate.tests import fixture
from migrate.tests.fixture.warnings import catch_warnings
from migrate.versioning.util import *
from migrate.versioning import api

import warnings

class TestUtil(fixture.Pathed):

    def test_construct_engine(self):
        """Construct engine the smart way"""
        url = 'sqlite://'

        engine = construct_engine(url)
        self.assertTrue(engine.name == 'sqlite')

        # keyword arg
        engine = construct_engine(url, engine_arg_encoding='utf-8')
        self.assertEqual('utf-8', engine.dialect.encoding)

        # dict
        engine = construct_engine(url, engine_dict={'encoding': 'utf-8'})
        self.assertEqual('utf-8', engine.dialect.encoding)

        # engine parameter
        engine_orig = create_engine('sqlite://')
        engine = construct_engine(engine_orig)
        self.assertEqual(engine_orig, engine)

        # test precedance
        engine = construct_engine(url, engine_dict={'encoding': 'iso-8859-1'},
            engine_arg_encoding='utf-8')
        self.assertEqual('utf-8', engine.dialect.encoding)

        # deprecated echo=True parameter
        try:
            # py 2.4 compatibility :-/
            cw = catch_warnings(record=True)
            w = cw.__enter__()

            warnings.simplefilter("always")
            engine = construct_engine(url, echo='True')
            self.assertTrue(engine.echo)

            self.assertEqual(1, len(w))
            self.assertTrue(issubclass(w[-1].category,
                                       MigrateDeprecationWarning))
            self.assertEqual(str(w[-1].message), 
                'echo=True parameter is deprecated, pass '
                'engine_arg_echo=True or engine_dict={"echo": True}')

        finally:
            cw.__exit__()

        # unsupported argument
        self.assertRaises(ValueError, construct_engine, 1)

    def test_passing_engine(self):
        repo = self.tmp_repos()
        api.create(repo, 'temp')
        api.script('First Version', repo)
        engine = construct_engine('sqlite:///:memory:')

        api.version_control(engine, repo)
        api.upgrade(engine, repo)

    def test_asbool(self):
        """test asbool parsing"""
        result = asbool(True)
        self.assertEqual(True, result)

        result = asbool(False)
        self.assertEqual(False, result)

        result = asbool('y')
        self.assertEqual(True, result)

        result = asbool('n')
        self.assertEqual(False, result)

        self.assertRaises(ValueError, asbool, 'test')
        self.assertRaises(ValueError, asbool, object)


    def test_load_model(self):
        """load model from dotted name"""
        model_path = os.path.join(self.temp_usable_dir, 'test_load_model.py')

        f = open(model_path, 'w')
        f.write("class FakeFloat(int): pass")
        f.close()

        try:
            # py 2.4 compatibility :-/
            cw = catch_warnings(record=True)
            w = cw.__enter__()

            warnings.simplefilter("always")

            # deprecated spelling
            FakeFloat = load_model('test_load_model.FakeFloat')
            self.assertTrue(isinstance(FakeFloat(), int))

            self.assertEqual(1, len(w))
            self.assertTrue(issubclass(w[-1].category,
                                       MigrateDeprecationWarning))
            self.assertEqual(str(w[-1].message),
                'model should be in form of module.model:User '
                'and not module.model.User')

        finally:
            cw.__exit__()

        FakeFloat = load_model('test_load_model:FakeFloat')
        self.assertTrue(isinstance(FakeFloat(), int))

        FakeFloat = load_model(FakeFloat)
        self.assertTrue(isinstance(FakeFloat(), int))

    def test_guess_obj_type(self):
        """guess object type from string"""
        result = guess_obj_type('7')
        self.assertEqual(7, result)

        result = guess_obj_type('y')
        self.assertEqual(True, result)

        result = guess_obj_type('test')
        self.assertEqual('test', result)
