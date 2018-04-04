Defining Custom Types
=====================

Special constraints can be imposed with this handy decorater.

datatyping.customtype
---------------------

.. autofunction:: datatyping.datatyping.customtype

Example
-------

The following example defines a "custom type", that can only be positive
integers.

.. code-block:: python

    from datatyping import validate, customtype
    @customtype
    def positive_int(i):
        if i < 1:
            raise TypeError('%d is not positive' % i)

    validate([positive_int], [1, 2, 3, 4])
    validate([positive_int], [1, 2, 3, -4])
    TypeError: -4 is not positive
