:mod:`migrate` - SQLAlchemy Migrate (schema change management)
==============================================================

.. module:: migrate
.. moduleauthor:: Evan Rosson

:Author: Evan Rosson
:Maintainer: Domen Kožar <domenNO@SPAMdev.si>
:Maintainer: Jan Dittberner <jan.dittbernerNO@SPAMgooglemail.com>
:Issues: http://code.google.com/p/sqlalchemy-migrate/issues/list
:Source Code: http://code.google.com/p/sqlalchemy-migrate/
:CI Tool: http://jenkins.gnuviech-server.de/job/sqlalchemy-migrate-all/
:Generated: |today|
:License: MIT
:Version: |release|


.. topic:: Overview

    Inspired by Ruby on Rails' migrations, SQLAlchemy Migrate provides a way to
    deal with database schema changes in SQLAlchemy_ projects.

    Migrate was started as part of `Google's Summer of Code`_ by Evan Rosson,
    mentored by Jonathan LaCour.

    The project was taken over by a small group of volunteers when Evan had no
    free time for the project. It is now hosted as a `Google Code project`_.
    During the hosting change the project was renamed to SQLAlchemy Migrate.

    Currently, sqlalchemy-migrate supports Python versions from 2.6 to 2.7.
    SQLAlchemy Migrate 0.7.2 supports SQLAlchemy 0.6.x and 0.7.x branches.

    Support for Python 2.4 and 2.5 as well as SQLAlchemy 0.5.x has been dropped
    after sqlalchemy-migrate 0.7.1.

.. warning::

    Version **0.6** broke backward compatibility, please read :ref:`changelog
    <backwards-06>` for more info.


Download and Development
------------------------

.. toctree::

   download
   credits


.. _dialect-support:

Dialect support
---------------

.. list-table::
    :header-rows: 1
    :widths: 25 10 10 10 10 10 11

    * - Operation / Dialect
      - :ref:`sqlite <sqlite-d>`
      - :ref:`postgres <postgres-d>`
      - :ref:`mysql <mysql-d>`
      - :ref:`oracle  <oracle-d>`
      - :ref:`firebird <firebird-d>`
      - mssql
    * - :ref:`ALTER TABLE RENAME TABLE <table-rename>`
      - yes
      - yes
      - yes
      - yes
      - no
      - not supported
    * - :ref:`ALTER TABLE RENAME COLUMN <column-alter>`
      - yes (workaround) [#1]_
      - yes
      - yes
      - yes
      - yes
      - not supported
    * - :ref:`ALTER TABLE ADD COLUMN <column-create>`
      - yes (workaround) [#2]_
      - yes
      - yes
      - yes
      - yes
      - not supported
    * - :ref:`ALTER TABLE DROP COLUMN <column-drop>`
      - yes (workaround) [#1]_
      - yes
      - yes
      - yes
      - yes
      - not supported
    * - :ref:`ALTER TABLE ALTER COLUMN <column-alter>`
      - yes (workaround) [#1]_
      - yes
      - yes
      - yes (with limitations) [#3]_
      - yes [#4]_
      - not supported
    * - :ref:`ALTER TABLE ADD CONSTRAINT <constraint-tutorial>`
      - partial (workaround) [#1]_
      - yes
      - yes
      - yes
      - yes
      - not supported
    * - :ref:`ALTER TABLE DROP CONSTRAINT <constraint-tutorial>`
      - partial (workaround) [#1]_
      - yes
      - yes
      - yes
      - yes
      - not supported
    * - :ref:`RENAME INDEX <index-rename>`
      - no
      - yes
      - no
      - yes
      - yes
      - not supported


.. [#1] Table is renamed to temporary table, new table is created followed by
        INSERT statements.
.. [#2] See http://www.sqlite.org/lang_altertable.html for more information.
        In cases not supported by sqlite, table is renamed to temporary table,
        new table is created followed by INSERT statements.
.. [#3] You can not change datatype or rename column if table has NOT NULL
        data, see http://blogs.x2line.com/al/archive/2005/08/30/1231.aspx for
        more information.
.. [#4] Changing nullable is not supported


Tutorials
--------------

List of useful tutorials:

* `Using migrate with Elixir <http://www.karoltomala.com/blog/?p=633>`_
* `Developing with migrations
  <http://caneypuggies.alwaysreformed.com/wiki/DevelopingWithMigrations>`_


User guide
-------------

SQLAlchemy Migrate is split into two parts, database schema versioning
(:mod:`migrate.versioning`) and database migration management
(:mod:`migrate.changeset`).  The versioning API is available as the
:ref:`migrate <command-line-usage>` command.

.. toctree::

   versioning
   changeset
   tools
   faq
   glossary

.. _`google's summer of code`: http://code.google.com/soc
.. _`Google Code project`: http://code.google.com/p/sqlalchemy-migrate
.. _sqlalchemy: http://www.sqlalchemy.org


API Documentation
------------------

.. toctree::

   api


Changelog
---------

.. toctree::

   changelog


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
