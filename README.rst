============
Coffee Flask
============

Coffee scheduler web application.

Setup
=====
Check out from github::

    git clone git://gihub.com/brookst/coffee_flask

VirtualEnv
----------
`VirtualEnv`_ makes setting up python package dependencies much easier. To install; see the `Virtual env docs`_. `VirtualEnv`_ is packaged as `python-virtualenv`_ on `Ubuntu`_ systems.
Set up a virtual environment using the following::

    mkvirtualenv -a `pwd` -r requirements.txt coffee_flask
    workon coffee_flask

To deactivate the `VirtualEnv`_, run ``deactivate``. To work on the environment again; run ``workon coffee_flask`` again.

.. _Virtual env docs: http://virtualenv.readthedocs.org/en/latest/virtualenv.html#installation
.. _python-virtualenv: http://packages.ubuntu.com/utopic/python/python-virtualenv
.. _Ubuntu: http://www.ubuntu.com/

Standalone running
------------------
Run the ``coffee_flask.py`` script as::

    python coffee_flask.py

Messages will be printed to the console and the application will be available on http://localhost:5000/

