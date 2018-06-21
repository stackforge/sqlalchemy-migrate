Download
--------

You can get the latest version of SQLAlchemy Migrate from its
`GitHub repository`_, `PyPI project page`_, or via pip_::

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
.. _sqlalchemy: http://www.sqlalchemy.org/download.html
.. _`GitHub repository`: https://github.com/openstack/sqlalchemy-migrate
.. _`PyPI project page`: https://pypi.org/project/sqlalchemy-migrate/
.. _`openstack-dev`: http://lists.openstack.org/cgi-bin/mailman/listinfo/openstack-dev

.. _development:

Development
-----------

If you would like to contribute to the development of OpenStack,
you must follow the steps in this page:

   http://docs.openstack.org/infra/manual/developers.html

Once those steps have been completed, changes to OpenStack
should be submitted for review via the Gerrit tool, following
the workflow documented at:

   http://docs.openstack.org/infra/manual/developers.html#development-workflow

Pull requests submitted through GitHub will be ignored.

Bugs should be filed on Launchpad, not GitHub:

   https://bugs.launchpad.net/sqlalchemy-migrate
