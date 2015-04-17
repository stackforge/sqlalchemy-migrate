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
are released, subscribe to `openstack-dev`_.

.. _pip: http://pip.openplans.org/
.. _easy_install: http://peak.telecommunity.com/DevCenter/EasyInstall#installing-easy-install
.. _sqlalchemy: http://www.sqlalchemy.org/download.html
.. _`cheese shop`: http://pypi.python.org/pypi/sqlalchemy-migrate
.. _`openstack-dev`: http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-dev

.. _development:

Development
-----------

Migrate's Mercurial_ repository is located at `Google Code`_.

To get the latest trunk::

 $ hg clone http://sqlalchemy-migrate.googlecode.com/hg/

Patc
.. _nose: http://readthedocs.org/docs/nose/
