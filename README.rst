pyjection
=========

|Software License| |Build Status| |Code Coverage| |Code Quality|

Pyjection is a lightweight python dependency injection library


Basic dependency injection
~~~~~~~~~~~~~~~~~~~~~~~~~~

The most import class is ``DependencyInjector`` which lets us register classes and retrieve instances.

.. code:: python

    from pyjection.dependency_injector import DependencyInjector

    class OuterClass(object):

        def __init__(self, inner_class):
            self.inner_class = inner_class

    class InnerClass(object):

        def __init__(self):
            self.foo = "bar"

    container = DependencyInjector()
    container.register(InnerClass)
    container.register(OuterClass)

    outer = container.get("outer_class")
    print(outer.inner_class.foo) # Will print "bar"

Class bindings
~~~~~~~~~~~~~~

Implicit class bindings
-----------------------

When no id is specified in the ``register`` method Pyjection creates implicit bindings for classes.
The implicit bindings assume your code follows PEP8 conventions: your classes are named in ``CamelCase``,
and your args are named in ``lower_with_underscores``.  Pinject transforms
class names to injectable arg names by lowercasing words and connecting them
with underscores.

+-------------+-------------+
| Class name  | Arg name    |
+=============+=============+
| ``Foo``     | ``foo``     |
+-------------+-------------+
| ``FooBar``  | ``foo_bar`` |
+-------------+-------------+

Explicit class bindings
-----------------------

It is also possible to manually set the id of a class when during its registration by specifying it as a second arguments.

.. code:: python

    container.register(FooClass, "inner_class")

With the example above, ``FooClass`` will later be injected to arguments named ``inner_class``

Instance retrieval
~~~~~~~~~~~~~~~~~~

To retrieve an instance of a class from the dependency injector 2 options are available in the ``get`` method:

* Specify the ``lower_with_underscores`` name of the class as a string
* Give the class as parameter

.. code:: python

    from pyjection.dependency_injector import DependencyInjector

    class FooClass(object):
        pass

    container = DependencyInjector()
    container.register(FooClass)

    container.get("foo_class")
    # Same as
    container.get(FooClass)

Singleton injection
~~~~~~~~~~~~~~~~~~~

The dependency injector lets us register a singleton. 
To register a singleton the method register_singleton may be used.
It takes the same arguments as register.

.. code:: python

    from pyjection.dependency_injector import DependencyInjector

    class SingletonClass(object):
        pass

    container = DependencyInjector()
    container.register_singleton(SingletonClass)
    # Or we could specify an id
    container.register_singleton(SingletonClass, "other_id")

    class_1 = container.get("other_id")
    class_2 = container.get("other_id")
    print(class_1 is class_2) # True


Explicit argument specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simple argument specification
-----------------------------

Sometimes the argument we need to inject is not an instance of a class.
The ``register`` and ``register_singleton`` methods return a service object that lets us specify what we want to bind to a given argument by using the ``add_argument`` method.

.. code:: python

    from pyjection.dependency_injector import DependencyInjector

    class FooClass(object):

        def __init__(self, foo):
            self.foo = foo

    container = DependencyInjector()
    service = container.register(FooClass)
    service.add_argument("foo", "bar")

    foo_class = container.get("foo_class")
    print(foo_class.foo) # Will print bar


Reference argument specification
--------------------------------

A service argument can also reference another dependency injector service.
It is useful when we want to inject a class not matching the argument name.

.. code:: python

    from pyjection.dependency_injector import DependencyInjector
    from pyjection.reference import Reference

    class OuterClass(object):

        def __init__(self, inner_class):
            self.inner_class = inner_class

    class FooClass(object):

        def __init__(self):
            self.foo = "bar"

    container = DependencyInjector()
    container.register(FooClass)
    container.register(OuterClass).add_argument("inner_class", Reference('foo_class'))

    instance = container.get(OuterClass)
    print(instance.inner_class.foo) # Will print bar
    

.. |Software License| image:: https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square
   :target: LICENSE
.. |Build Status| image:: https://scrutinizer-ci.com/g/Darkheir/pyjection/badges/build.png?b=master
   :target: https://scrutinizer-ci.com/g/Darkheir/pyjection/build-status/master
.. |Code Coverage| image:: https://scrutinizer-ci.com/g/Darkheir/pyjection/badges/coverage.png?b=master
   :target: https://scrutinizer-ci.com/g/Darkheir/pyjection/?branch=master
.. |Code Quality| image:: https://scrutinizer-ci.com/g/Darkheir/pyjection/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/Darkheir/pyjection/?branch=master
