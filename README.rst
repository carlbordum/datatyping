datatyping
==========

.. image:: https://travis-ci.org/Zaab1t/datatyping.svg?branch=master
    :target: https://travis-ci.org/Zaab1t/datatyping

.. image:: https://readthedocs.org/projects/datatyping/badge/?version=latest
    :target: http://datatyping.readthedocs.io


Datatyping is a (pure) Python library with no dependencies that you can use to
verify whether elements in a data structure has the expected types. Great for
incomming json.

.. code-block:: python

    import datatyping
    datatyping.validate([int], [1, 2, 3])

Check out the `documentation <http://datatyping.readthedocs.io>`_ for examples,
installation instructions and usage.


Develop with me :)
------------------

Fork the repo first. Use the following lines to setup

.. code-block:: bash

    $ git clone https://github.com/your_name/datatyping
    $ cd datatyping
    $ virtualenv venv
    $ . venv/bin/activate
    $ python setup.py develop

Run tests

.. code-block:: bash

    $ pip install pytest
    $ python -m pytest

Build documentation

.. code-block:: bash

    $ make -C docs/ html


Notes
-----
* Inspired by `"How Python Makes Working With Data More Difficult in the Long Run" <https://jeffknupp.com/blog/2016/11/13/how-python-makes-working-with-data-more-difficult-in-the-long-run/>`_.
* Any and all contributions are welcome.
* Please open an issue if you need help (read: I messed up).
* Suggest anything you want to see support for!
