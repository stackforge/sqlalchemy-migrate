#!/usr/bin/env python
# -*- coding: utf-8 -*-

from migrate.exceptions import *
from migrate.versioning.version import *

from migrate.tests import fixture


class TestVerNum(fixture.Base):
    def test_invalid(self):
        """Disallow invalid version numbers"""
        versions = ('-1', -1, 'Thirteen', '')
        for version in versions:
            self.assertRaises(ValueError, VerNum, version)

    def test_str(self):
        """Test str and repr version numbers"""
        self.assertEqual('2', str(VerNum(2)))
        self.assertEqual('<VerNum(2)>', repr(VerNum(2)))

    def test_is(self):
        """Two version with the same number should be equal"""
        a = VerNum(1)
        b = VerNum(1)
        self.assertTrue(a is b)

        self.assertEqual(VerNum(2), VerNum(VerNum(2)))

    def test_add(self):
        self.assertEqual(VerNum(2), VerNum(1) + VerNum(1))
        self.assertEqual(2, VerNum(1) + 1)
        self.assertEqual('2', VerNum(1) + 1)
        self.assertTrue(isinstance(VerNum(1) + 1, VerNum))

    def test_sub(self):
        self.assertEqual(0, VerNum(1) - 1)
        self.assertTrue(isinstance(VerNum(1) - 1, VerNum))
        self.assertRaises(ValueError, lambda: VerNum(0) - 1)

    def test_eq(self):
        """Two versions are equal"""
        self.assertEqual(VerNum('1'), VerNum(1))
        self.assertEqual(1, VerNum(1))
        self.assertEqual('1', VerNum(1))
        self.assertNotEqual(VerNum(1), 2)

    def test_ne(self):
        self.assertTrue(VerNum(1) != 2)
        self.assertFalse(VerNum(1) != 1)

    def test_lt(self):
        self.assertFalse(VerNum(1) < 1)
        self.assertTrue(VerNum(1) < 2)
        self.assertFalse(VerNum(2) < 1)

    def test_le(self):
        self.assertTrue(VerNum(1) <= 1)
        self.assertTrue(VerNum(1) <= 2)
        self.assertFalse(VerNum(2) <= 1)

    def test_gt(self):
        self.assertFalse(VerNum(1) > 1)
        self.assertFalse(VerNum(1) > 2)
        self.assertTrue(VerNum(2) > 1)

    def test_ge(self):
        self.assertTrue(VerNum(1) >= 1)
        self.assertTrue(VerNum(2) >= 1)
        self.assertFalse(VerNum(1) >= 2)

    def test_int_cast(self):
        ver = VerNum(3)
        # test __int__
        self.assertEqual(3, int(ver))
        # test __index__: range() doesn't call __int__
        self.assertEqual([], list(range(ver, ver)))


class TestVersion(fixture.Pathed):

    def setUp(self):
        super(TestVersion, self).setUp()

    def test_str_to_filename(self):
        self.assertEqual('', str_to_filename(''))
        self.assertEqual('_', str_to_filename('__'))
        self.assertEqual('a', str_to_filename('a'))
        self.assertEqual('Abc_Def', str_to_filename('Abc Def'))
        self.assertEqual('Abc_D_Ef', str_to_filename('Abc "D" Ef'))
        self.assertEqual('Abc_s_Stuff', str_to_filename("Abc's Stuff"))
        self.assertEqual('a_b', str_to_filename("a      b"))
        self.assertEqual('a_b_to_c', str_to_filename("a.b to c"))

    def test_collection(self):
        """Let's see how we handle versions collection"""
        coll = Collection(self.temp_usable_dir)
        coll.create_new_python_version("foo bar")
        coll.create_new_sql_version("postgres", "foo bar")
        coll.create_new_sql_version("sqlite", "foo bar")
        coll.create_new_python_version("")

        self.assertEqual(4, coll.latest)
        self.assertEqual(4, len(coll.versions))
        self.assertEqual(coll.version(coll.latest), coll.version(4))
        # Check for non-existing version
        self.assertRaises(VersionNotFoundError, coll.version, 5)
        # Check for the current version
        self.assertEqual(coll.version(4).version, '4')

        coll2 = Collection(self.temp_usable_dir)
        self.assertEqual(coll2.versions, coll.versions)

        Collection.clear()

    def test_old_repository(self):
        open(os.path.join(self.temp_usable_dir, '1'), 'w')
        self.assertRaises(Exception, Collection, self.temp_usable_dir)

    #TODO: def test_collection_unicode(self):
    #    pass

    def test_create_new_python_version(self):
        coll = Collection(self.temp_usable_dir)
        coll.create_new_python_version("'")

        ver = coll.version()
        self.assertTrue(ver.script().source())

    def test_create_new_sql_version(self):
        coll = Collection(self.temp_usable_dir)
        coll.create_new_sql_version("sqlite", "foo bar")

        ver = coll.version()
        ver_up = ver.script('sqlite', 'upgrade')
        ver_down = ver.script('sqlite', 'downgrade')
        ver_up.source()
        ver_down.source()

    def test_selection(self):
        """Verify right sql script is selected"""

        # Create empty directory.
        path = self.tmp_repos()
        os.mkdir(path)

        # Create files -- files must be present or you'll get an exception later.
        python_file = '001_initial_.py'
        sqlite_upgrade_file = '001_sqlite_upgrade.sql'
        default_upgrade_file = '001_default_upgrade.sql'
        for file_ in [sqlite_upgrade_file, default_upgrade_file, python_file]:
            filepath = '%s/%s' % (path, file_)
            open(filepath, 'w').close()

        ver = Version(1, path, [sqlite_upgrade_file])
        self.assertEqual(sqlite_upgrade_file, os.path.basename(ver.script('sqlite', 'upgrade').path))

        ver = Version(1, path, [default_upgrade_file])
        self.assertEqual(default_upgrade_file, os.path.basename(ver.script('default', 'upgrade').path))

        ver = Version(1, path, [sqlite_upgrade_file, default_upgrade_file])
        self.assertEqual(sqlite_upgrade_file, os.path.basename(ver.script('sqlite', 'upgrade').path))

        ver = Version(1, path, [sqlite_upgrade_file, default_upgrade_file, python_file])
        self.assertEqual(default_upgrade_file, os.path.basename(ver.script('postgres', 'upgrade').path))

        ver = Version(1, path, [sqlite_upgrade_file, python_file])
        self.assertEqual(python_file, os.path.basename(ver.script('postgres', 'upgrade').path))

    def test_bad_version(self):
        ver = Version(1, self.temp_usable_dir, [])
        self.assertRaises(ScriptError, ver.add_script, '123.sql')

        # tests bad ibm_db_sa filename
        ver = Version(123, self.temp_usable_dir, [])
        self.assertRaises(ScriptError, ver.add_script,
                          '123_ibm_db_sa_upgrade.sql')

        # tests that the name is ok but the script doesn't exist
        self.assertRaises(InvalidScriptError, ver.add_script,
                          '123_test_ibm_db_sa_upgrade.sql')

        pyscript = os.path.join(self.temp_usable_dir, 'bla.py')
        open(pyscript, 'w')
        ver.add_script(pyscript)
        self.assertRaises(ScriptError, ver.add_script, 'bla.py')
