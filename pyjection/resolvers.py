"""
Module that contains all the resolvers.

A resolver is a class that is able to retrieve a dependency to inject.
"""

from pyjection.reference import Reference


class BaseResolver(object):
    """
    Base class for the resolvers
    """

    def resolve(self, method_parameter, service, injector):
        raise NotImplementedError('This method must be implemented')


class ServiceResolver(BaseResolver):
    """
    Try to resolve the dependency based on
    the service that has been provided to the injector.
    """

    def resolve(self, method_parameter, service, injector):
        if method_parameter.name not in service.arguments:
            return None

        value = service.arguments[method_parameter.name]
        if not isinstance(value, Reference):
            return value
        # The value references an other dependency service
        if value.return_class:
            return injector.get_uninstantiated(value.name)
        return injector.get(value.name)


class NameResolver(BaseResolver):
    """
    Try to resolve the dependency based on the parameter name.

    If the latter is declared in the dependency injector then we retrieve it
    as the instance to inject.
    """

    def resolve(self, method_parameter, service, injector):
        if injector.has_service(method_parameter.name):
            return injector.get(method_parameter.name)
