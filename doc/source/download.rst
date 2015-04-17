Download
--------

You can get the latest version of SQLAlchemy Migrate from the
`project's download page`_, the `cheese shop`_, pip_ or via easy_install_::

 $ easy_install sqlalchemy-migrate

or::

 $ pip install sqlalchemy-migrate

You should now be able to use the :command:`migrate` command from the command
line::

 $ migrate

This should list all available commands. To get more information regarding a
command use::

 $ migrate help COMMAND

If you'd like to be notified when new versions of SQLAlchemy Migrate
are released, subscribe to `migrate-announce`_.

.. _pip: http://pip.openplans.org/
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall#installing-easy-install
.. _sqlalchemy: http://www.sqlalchemy.org/download.html
.. _`cheese shop`: http://pypi.python.org/pypi/sqlalchemy-migrate
.. _`migrate-announce`: http://groups.google.com/group/migrate-announce

.. _development:

Development
-----------

Migrate's Mercurial_ repository is located at `Google Code`_.

To get the latest trunk::

 $ hg clone http://sqlalchemy-migrate.googlecode.com/hg/

Patches should be submitted to the `issue tracker`_. You are free to create
your own clone to provide your patches. We are open to pull requests in our
`issue tracker`_.

If you want to work on sqlalchemy-migrate you might want to use a `virtualenv`.

To run the included test suite you have to copy :file:`test_db.cfg.tmpl` to
:file:`test_db.cfg` and put SQLAlchemy database URLs valid for your environment
into that file. We use `nose`_ for our tests and include a test requirements
file for pip. You might use the following commands to install the test
requirements and run the tests::

 $ pip install -r test-req.pip
 $ python setup.py develop
 $ python setup.py nosetests

If you are curious about status changes of sqlalchemy-migrate's issues you
might want to subscribe to `sqlalchemy-migrate-issues`_.

We use a `Jenkins CI`_ continuous integration tool installation to
help us run tests on most of the databases that migrate supports.

.. _Mercurial: http://www.mercurial-scm.org/
.. _Google Code: http://sqlalchemy-migrate.googlecode.com/hg/
.. _issue tracker: http://code.google.com/p/sqlalchemy-migrate/issues/list
.. _sqlalchemy-migrate-issues: http://groups.google.com/group/sqlalchemy-migrate-issues
.. _Jenkins CI: http://jenkins.gnuviech-server.de/job/sqlalchemy-migrate-all/
.. _nose: http://readthedocs.org/docs/nose/
