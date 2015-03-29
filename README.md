# pyjection

[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE)
[![Build Status](https://scrutinizer-ci.com/g/Darkheir/pyjection/badges/build.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/pyjection/build-status/master)
[![Code Coverage](https://scrutinizer-ci.com/g/Darkheir/pyjection/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/pyjection/?branch=master)
[![Code Quality](https://scrutinizer-ci.com/g/Darkheir/pyjection/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Darkheir/pyjection/?branch=master)


Pyjection is a lightweight python dependency injection library


## Examples

### Basic example

```python
# Import the required dependency
from pyjection.dependency_injector import DependencyInjector

#For the sake of this example we create a dummy class
class A(object):

    def __init__(self, parameter):
        print("A has been instantiated with param: %s" % (parameter))


# Instantiate the dependency injector
container = DependencyInjector()

# We register the class A in the dependency injector
service = container.register("a_class", A)
# And we specify its parameter value
service.add_argument("parameter", "my_value")

#We could have chained the argument add to the registration:
container.register("a_class", A).add_argument("parameter", "my_value")

# Now we ask the dependency injector to generate an instance of A
# It will print "A has been instantiated with param: my_value"
a_instance = container.get("a_class")
#If we call again container.get("a_class") a new instance will be returned
```

### Singleton example

The dependency injector lets us register a singleton. The same instance will the be returned when asked

```python
# Import the required dependency
from pyjection.dependency_injector import DependencyInjector

#For the sake of this example we create a dummy class
class A(object):

    def __init__(self, parameter):
        print("A has been instantiated with param: %s" % (parameter))


# Instantiate the dependency injector
container = DependencyInjector()

# We register the class A in the dependency injector
service = container.register_singleton("a_singleton", A)
# And we specify its parameter value
service.add_argument("parameter", "my_value")

# Now we ask the dependency injector to get an instance of A
# It will print "A has been instantiated with param: my_value"
a1_instance = container.get("a_singleton")
# We ask again an instance, nothing will be print since the same
# instance is returned
a2_instance = container.get("a_singleton")
```

### Instance example

We can also use the dependency injector to retrieve an already instantiated instance

```python
# Import the required dependency
from pyjection.dependency_injector import DependencyInjector

#For the sake of this example we create a dummy class
class A(object):

    def __init__(self, parameter):
        print("A has been instantiated with param: %s" % (parameter))

a_instance = A('my_value')

# Instantiate the dependency injector
container = DependencyInjector()
# We register the already instantiated object
service = container.register("a_instance", a)

# Now we ask the dependency injector to get the instance
a1_instance = container.get("a_instance")

# Will print True
print(a1_instance == a_instance)
```

### Reference example

A service argument can reference another dependency injector service

```python
from pyjection.dependency_injector import DependencyInjector
from pyjection.reference import Reference

#For the sake of this example we create 2 dummy classes
class A(object):

    def __init__(self, parameter):
        print("A has been instantiated with param: %s" % (parameter))

class B(object):

    def __init__(self, a_parameter):
        if isinstance(a_parameter, A):
            print('B has been instantiated with an instance of A')


# Instantiate the dependency injector
container = DependencyInjector()

# We register the class A in the dependency injector
container.register("a_instance", A).add_argument("parameter", "my_value")

# We register B and specify that "a_parameter" will reference the service "a_instance"
container.register("b_instance", B).add_argument("a_parameter", Reference('a_instance'))


# This will instantiate an instance of A and pass it has parameter to B
b_instance = container.get("b_instance")
```

Using this approach a lot can be done automatically.

For example we could do the following: when asking for a D class it will instantiates a C class needed as parameter that itself takes 2 classes A and B as arguments.

## Available attributes and methods

In the DependencyInjector class:

* register(identifier, subject) : Register a new service in the dependency injector for the given subject. This service can be
    * A class that will be instantiated when asked
    * An already instantiated instance that will be returned as it is
    
* register_singleton(identifier, subject) : Register a new service as a singleton. So the same instance will be returned each time the service is asked

* has_service(identifier) : Check if the dependency injector already has this service declared

* get(identifier) : Return an instance of the service subject.

In the service class:

* is_singleton : Wether the declared service is a singleton
* type: The service type. It can be 'class' or 'instance'
* add_argument(name, value): Add an argument to the service. An argument value can be a Reference to another service
* add_arguments(**kwargs): Add severals arguments to the service
