#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.util import *
from sqlalchemy.exc import *

from migrate.exceptions import *
from migrate.changeset import *
from migrate.changeset.databases import sqlite

from migrate.tests import fixture


def uniques(*constraints):
    """Make a sequence of UniqueConstraint instances easily comparable

        Convert a sequence of UniqueConstraint instances into a set of
        tuples of form (constraint_name, (constraint_columns)) so that
        assertEquals() will be able to compare sets of unique constraints

    """

    return set((uc.name, tuple(uc.columns.keys())) for uc in constraints)


class CommonTestConstraint(fixture.DB):
    """helper functions to test constraints.
    
    we just create a fresh new table and make sure everything is
    as required.
    """

    def _setup(self, url):
        super(CommonTestConstraint, self)._setup(url)
        self._create_table()

    def _teardown(self):
        if hasattr(self, 'table') and self.engine.has_table(self.table.name):
            self.table.drop()
        if hasattr(self, 'table2') and self.engine.has_table(self.table2.name):
            self.table2.drop()
        super(CommonTestConstraint, self)._teardown()

    def _create_table(self):
        self._connect(self.url)
        self.meta = MetaData(self.engine)
        self.tablename = 'mytable'
        self.table = Table(self.tablename, self.meta,
            Column(u'id', Integer, nullable=False),
            Column(u'fkey', Integer, nullable=False),
            mysql_engine='InnoDB')
        if self.engine.has_table(self.table.name):
            self.table.drop()
        self.table.create()

        self.table2 = Table(
            'table2',
            MetaData(self.engine),
            Column('a', Integer),
            Column('b', String(10)),
            Column('c', Integer),
            UniqueConstraint('a', 'b', name='unique_a_b'),
            UniqueConstraint('b', 'c', name='unique_b_c')
        )
        if self.engine.has_table(self.table2.name):
            self.table2.drop()
        self.table2.create()

        # NOTE(rpodolyaka): it's important to use the reflected table here
        #                   rather than original one because this is what
        #                   we actually do in db migrations code
        self.reflected_table2 = Table(
            'table2',
            MetaData(self.engine),
            autoload=True
        )

        # make sure we start at zero
        self.assertEqual(len(self.table.primary_key), 0)
        self.assert_(isinstance(self.table.primary_key,
            schema.PrimaryKeyConstraint), self.table.primary_key.__class__)


class TestConstraint(CommonTestConstraint):
    level = fixture.DB.CONNECT

    def _define_pk(self, *cols):
        # Add a pk by creating a PK constraint
        if (self.engine.name in ('oracle', 'firebird')):
            # Can't drop Oracle PKs without an explicit name
            pk = PrimaryKeyConstraint(table=self.table, name='temp_pk_key', *cols)
        else:
            pk = PrimaryKeyConstraint(table=self.table, *cols)
        self.compare_columns_equal(pk.columns, cols)
        pk.create()
        self.refresh_table()
        if not self.url.startswith('sqlite'):
            self.compare_columns_equal(self.table.primary_key, cols, ['type', 'autoincrement'])

        # Drop the PK constraint
        #if (self.engine.name in ('oracle', 'firebird')):
        #    # Apparently Oracle PK names aren't introspected
        #    pk.name = self.table.primary_key.name
        pk.drop()
        self.refresh_table()
        self.assertEqual(len(self.table.primary_key), 0)
        self.assert_(isinstance(self.table.primary_key, schema.PrimaryKeyConstraint))
        return pk

    @fixture.usedb(not_supported='sqlite')
    def test_define_fk(self):
        """FK constraints can be defined, created, and dropped"""
        # FK target must be unique
        pk = PrimaryKeyConstraint(self.table.c.id, table=self.table, name="pkid")
        pk.create()

        # Add a FK by creating a FK constraint
        if SQLA_07:
            self.assertEqual(list(self.table.c.fkey.foreign_keys), [])
        else:
            self.assertEqual(self.table.c.fkey.foreign_keys._list, [])
        fk = ForeignKeyConstraint([self.table.c.fkey],
                                  [self.table.c.id],
                                  name="fk_id_fkey",
                                  ondelete="CASCADE")
        if SQLA_07:
            self.assert_(list(self.table.c.fkey.foreign_keys) is not [])
        else:
            self.assert_(self.table.c.fkey.foreign_keys._list is not [])
        for key in fk.columns:
            self.assertEqual(key, self.table.c.fkey.name)
        self.assertEqual([e.column for e in fk.elements], [self.table.c.id])
        self.assertEqual(list(fk.referenced), [self.table.c.id])

        if self.url.startswith('mysql'):
            # MySQL FKs need an index
            index = Index('index_name', self.table.c.fkey)
            index.create()
        fk.create()

        # test for ondelete/onupdate
        if SQLA_07:
            fkey = list(self.table.c.fkey.foreign_keys)[0]
        else:
            fkey = self.table.c.fkey.foreign_keys._list[0]
        self.assertEqual(fkey.ondelete, "CASCADE")
        # TODO: test on real db if it was set

        self.refresh_table()
        if SQLA_07:
            self.assert_(list(self.table.c.fkey.foreign_keys) is not [])
        else:
            self.assert_(self.table.c.fkey.foreign_keys._list is not [])

        fk.drop()
        self.refresh_table()
        if SQLA_07:
            self.assertEqual(list(self.table.c.fkey.foreign_keys), [])
        else:
            self.assertEqual(self.table.c.fkey.foreign_keys._list, [])

    @fixture.usedb()
    def test_define_pk(self):
        """PK constraints can be defined, created, and dropped"""
        self._define_pk(self.table.c.fkey)

    @fixture.usedb()
    def test_define_pk_multi(self):
        """Multicolumn PK constraints can be defined, created, and dropped"""
        self._define_pk(self.table.c.id, self.table.c.fkey)

    @fixture.usedb(not_supported=['firebird'])
    def test_drop_cascade(self):
        """Drop constraint cascaded"""
        pk = PrimaryKeyConstraint('fkey', table=self.table, name="id_pkey")
        pk.create()
        self.refresh_table()

        # Drop the PK constraint forcing cascade
        pk.drop(cascade=True)

        # TODO: add real assertion if it was added

    @fixture.usedb(supported=['mysql'])
    def test_fail_mysql_check_constraints(self):
        """Check constraints raise NotSupported for mysql on drop"""
        cons = CheckConstraint('id > 3', name="id_check", table=self.table)
        cons.create()
        self.refresh_table()

        try:
            cons.drop()
        except NotSupportedError:
            pass
        else:
            self.fail()

    @fixture.usedb(not_supported=['sqlite', 'mysql'])
    def test_named_check_constraints(self):
        """Check constraints can be defined, created, and dropped"""
        self.assertRaises(InvalidConstraintError, CheckConstraint, 'id > 3')
        cons = CheckConstraint('id > 3', name="id_check", table=self.table)
        cons.create()
        self.refresh_table()

        self.table.insert(values={'id': 4, 'fkey': 1}).execute()
        try:
            self.table.insert(values={'id': 1, 'fkey': 1}).execute()
        except (IntegrityError, ProgrammingError):
            pass
        else:
            self.fail()

        # Remove the name, drop the constraint; it should succeed
        cons.drop()
        self.refresh_table()
        self.table.insert(values={'id': 2, 'fkey': 2}).execute()
        self.table.insert(values={'id': 1, 'fkey': 2}).execute()

    @fixture.usedb(supported=['sqlite'])
    def test_get_unique_constraints_sqlite(self):
        table = self.reflected_table2

        existing = uniques(*sqlite._get_unique_constraints(table))
        should_be = uniques(
            UniqueConstraint(table.c.a, table.c.b, name='unique_a_b'),
            UniqueConstraint(table.c.b, table.c.c, name='unique_b_c'),
        )

        self.assertEquals(should_be, existing)

    @fixture.usedb(supported=['sqlite'])
    def test_add_unique_constraint_sqlite(self):
        table = self.reflected_table2
        UniqueConstraint(table.c.a, table.c.c, name='unique_a_c').create()

        existing = uniques(*sqlite._get_unique_constraints(table))
        should_be = uniques(
            UniqueConstraint(table.c.a, table.c.b, name='unique_a_b'),
            UniqueConstraint(table.c.b, table.c.c, name='unique_b_c'),
            UniqueConstraint(table.c.a, table.c.c, name='unique_a_c'),
        )
        self.assertEquals(should_be, existing)

    @fixture.usedb(supported=['sqlite'])
    def test_drop_unique_constraint_sqlite(self):
        table = self.reflected_table2
        UniqueConstraint(table.c.a, table.c.b, name='unique_a_b').drop()

        existing = uniques(*sqlite._get_unique_constraints(table))
        should_be = uniques(
            UniqueConstraint(table.c.b, table.c.c, name='unique_b_c'),
        )
        self.assertEquals(should_be, existing)


class TestAutoname(CommonTestConstraint):
    """Every method tests for a type of constraint wether it can autoname
    itself and if you can pass object instance and names to classes.
    """
    level = fixture.DB.CONNECT

    @fixture.usedb(not_supported=['oracle', 'firebird'])
    def test_autoname_pk(self):
        """PrimaryKeyConstraints can guess their name if None is given"""
        # Don't supply a name; it should create one
        cons = PrimaryKeyConstraint(self.table.c.id)
        cons.create()
        self.refresh_table()
        if not self.url.startswith('sqlite'):
            # TODO: test for index for sqlite
            self.compare_columns_equal(cons.columns, self.table.primary_key, ['autoincrement', 'type'])

        # Remove the name, drop the constraint; it should succeed
        cons.name = None
        cons.drop()
        self.refresh_table()
        self.assertEqual(list(), list(self.table.primary_key))

        # test string names
        cons = PrimaryKeyConstraint('id', table=self.table)
        cons.create()
        self.refresh_table()
        if not self.url.startswith('sqlite'):
            # TODO: test for index for sqlite
            self.compare_columns_equal(cons.columns, self.table.primary_key)
        cons.name = None
        cons.drop()

    @fixture.usedb(not_supported=['oracle', 'sqlite', 'firebird'])
    def test_autoname_fk(self):
        """ForeignKeyConstraints can guess their name if None is given"""
        cons = PrimaryKeyConstraint(self.table.c.id)
        cons.create()

        cons = ForeignKeyConstraint([self.table.c.fkey], [self.table.c.id])
        cons.create()
        self.refresh_table()
        if SQLA_07:
            list(self.table.c.fkey.foreign_keys)[0].column is self.table.c.id
        else:
            self.table.c.fkey.foreign_keys[0].column is self.table.c.id

        # Remove the name, drop the constraint; it should succeed
        cons.name = None
        cons.drop()
        self.refresh_table()
        if SQLA_07:
            self.assertEqual(list(self.table.c.fkey.foreign_keys), list())
        else:
            self.assertEqual(self.table.c.fkey.foreign_keys._list, list())

        # test string names
        cons = ForeignKeyConstraint(['fkey'], ['%s.id' % self.tablename], table=self.table)
        cons.create()
        self.refresh_table()
        if SQLA_07:
            list(self.table.c.fkey.foreign_keys)[0].column is self.table.c.id
        else:
            self.table.c.fkey.foreign_keys[0].column is self.table.c.id

        # Remove the name, drop the constraint; it should succeed
        cons.name = None
        cons.drop()

    @fixture.usedb(not_supported=['oracle', 'sqlite', 'mysql'])
    def test_autoname_check(self):
        """CheckConstraints can guess their name if None is given"""
        cons = CheckConstraint('id > 3', columns=[self.table.c.id])
        cons.create()
        self.refresh_table()
    
        if not self.engine.name == 'mysql':
            self.table.insert(values={'id': 4, 'fkey': 1}).execute()
            try:
                self.table.insert(values={'id': 1, 'fkey': 2}).execute()
            except (IntegrityError, ProgrammingError):
                pass
            else:
                self.fail()

        # Remove the name, drop the constraint; it should succeed
        cons.name = None
        cons.drop()
        self.refresh_table()
        self.table.insert(values={'id': 2, 'fkey': 2}).execute()
        self.table.insert(values={'id': 1, 'fkey': 3}).execute()

    @fixture.usedb(not_supported=['oracle', 'sqlite'])
    def test_autoname_unique(self):
        """UniqueConstraints can guess their name if None is given"""
        cons = UniqueConstraint(self.table.c.fkey)
        cons.create()
        self.refresh_table()
    
        self.table.insert(values={'fkey': 4, 'id': 1}).execute()
        try:
            self.table.insert(values={'fkey': 4, 'id': 2}).execute()
        except (sqlalchemy.exc.IntegrityError,
                sqlalchemy.exc.ProgrammingError):
            pass
        else:
            self.fail()

        # Remove the name, drop the constraint; it should succeed
        cons.name = None
        cons.drop()
        self.refresh_table()
        self.table.insert(values={'fkey': 4, 'id': 2}).execute()
        self.table.insert(values={'fkey': 4, 'id': 1}).execute()
