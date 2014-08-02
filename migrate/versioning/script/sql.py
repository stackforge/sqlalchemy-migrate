#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import shutil

import sqlparse

from migrate.versioning.script import base
from migrate.versioning.template import Template


log = logging.getLogger(__name__)

class SqlScript(base.BaseScript):
    """A file containing plain SQL statements."""

    @classmethod
    def create(cls, path, **opts):
        """Create an empty migration script at specified path

        :returns: :class:`SqlScript instance <migrate.versioning.script.sql.SqlScript>`"""
        cls.require_notfound(path)

        src = Template(opts.pop('templates_path', None)).get_sql_script(theme=opts.pop('templates_theme', None))
        shutil.copy(src, path)
        return cls(path)

    # TODO: why is step parameter even here?
    def run(self, engine, step=None):
        """Runs SQL script through raw dbapi execute call"""
        text = self.source()
        # Don't rely on SA's autocommit here
        # (SA uses .startswith to check if a commit is needed. What if script
        # starts with a comment?)
        conn = engine.connect()
        try:
            trans = conn.begin()
            try:
                # NOTE(ihrachys): script may contain multiple statements, and
                # not all drivers reliably handle multistatement queries or
                # commands passed to .execute(), so split them and execute one
                # by one
                for statement in sqlparse.split(text):
                    if statement:
                        conn.execute(statement)
                trans.commit()
            except Exception as e:
                log.error("SQL script %s failed: %s", self.path, e)
                trans.rollback()
                raise
        finally:
            conn.close()
