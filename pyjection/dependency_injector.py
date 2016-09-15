import logging

from inspect import signature
from inspect import Parameter
from collections import OrderedDict

from pyjection.service import Service
from pyjection.reference import Reference
from pyjection.helper import get_service_subject_identifier


class DependencyInjector(object):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._services = dict()
        self._singletons = dict()

    def register(self, service_subject, identifier=None):
        """
        Register a new service in the dependency injector

        This service can be :
            * A class that will be instantiated when called
            * An already instantiated instance that will be returned

        If no identifier is passed, it will be the class name in snake_case

        :param service_subject: The class or instance
        :type service_subject: mixed
        :param identifier: The identifier used to later retrieve a service instance
        :type identifier: string

        :return: Return the newly created service entry
        :rtype: Service
        """
        if identifier is None:
            identifier = get_service_subject_identifier(service_subject)
        service = Service(service_subject)
        self._services[identifier] = service
        self._logger.debug(
            "Class %s registered with identifier %s",
            str(service_subject),
            identifier
        )
        return service

    def register_singleton(self, service_subject, identifier=None):
        """
        Register a new singleton service in in the dependency injector

        This service can be :
            * A class that will be instantiated when called
            * An already instantiated instance that will be returned

        If no identifier is passed, it will be the class name in snake_case

        :param service_subject: The class or instance
        :type service_subject: mixed
        :param identifier: The identifier used to later retrieve a service singleton
        :type identifier: string

        :return: Return the newly created dependency entry
        :rtype: Service
        """
        if identifier is None:
            identifier = get_service_subject_identifier(service_subject)
        service = Service(service_subject)
        service.is_singleton = True
        self._services[identifier] = service
        self._logger.debug(
            "Class %s registered as singleton with identifier %s",
            str(service_subject),
            identifier
        )
        return service

    def get(self, identifier):
        """
        Instantiate and retrieve the service matching this identifier

        If the service has been self has a singleton the same service object
        will be return each time this service is asked

        :param identifier: The identifier or the class to retrieve
        :type identifier: mixed
        :return: The instantiated object
        :rtype: mixed
        """
        if isinstance(identifier, str) is False:
            identifier = get_service_subject_identifier(identifier)

        if self.has_service(identifier) is False:
            self._logger.error("No service has been declared with ID %s", identifier)
            raise Exception("No service has been declared with this ID")

        service = self._services[identifier]
        instance = self._get_singleton(identifier, service)
        if instance is not None:
            self._logger.debug("Return singleton with ID %s", identifier)
            return instance

        instance = self._get_instance(service)
        self._set_singleton(identifier, instance, service)
        self._logger.debug("Return instance with ID %s", identifier)
        return instance

    def get_uninstantiated(self, identifier):
        if isinstance(identifier, str) is False:
            identifier = get_service_subject_identifier(identifier)

        if self.has_service(identifier) is False:
            self._logger.error("No service has been declared with ID %s", identifier)
            raise Exception("No service has been declared with this ID")

        service = self._services[identifier]
        return service.subject

    def has_service(self, identifier):
        """
        Check if the service matching the given identifier
        has already been declared

        :param identifier: Name of the service or the class
        :type identifier: mixed
        :return: Whether or not the service exists
        :rtype: boolean
        """
        if isinstance(identifier, str) is False:
            identifier = get_service_subject_identifier(identifier)

        if identifier in self._services:
            return True
        return False

    def _get_singleton(self, identifier, service):
        """
        Return the singleton if it has been setted and
        the service represents a singleton

        :param identifier: the singleton identifier
        :param service: The service we need the singleton for
        :type identifier: string
        :type service: Service

        :return: The singleton instance or None
        :rtype: mixed
        """
        if service.is_singleton is True and identifier in self._singletons:
            return self._singletons[identifier]
        return None

    def _set_singleton(self, identifier, instance, service):
        """
        Set the instance as a singleton in the dict
        if the service represents a singleton

        :param identifier: the singleton identifier
        :param service: The service we want to set a singleton for
        :param instance: The singleton instance
        :type identifier: string
        :type service: Service
        :type instance: mixed
        """
        if service.is_singleton is True:
            self._singletons[identifier] = instance

    def _get_instance(self, service):
        """
        Return the instantiated object for the given service

        :param service: The service we need an instance for
        :type service: Service
        :return: The instantiated object
        """
        if service.type == 'instance':
            return service.subject
        arguments = self._generate_arguments_dict(service)
        return service.subject(**arguments)

    def _generate_arguments_dict(self, service):
        """
        Generate a dict containing all the parameters values
        required to Instantiate the service.

        An exception is raised if a mandatory argument cannot be
        retrieved.

        :param service: The service that needs to be instantiated
        :type service: Service
        :return: The parameters values to use to instantiate the service
        :rtype: dict
        """
        arguments = dict()

        # We can't use signature on object __init__
        if self._is_object_init(service.subject) is True:
            return arguments

        sig = signature(service.subject.__init__)
        method_parameters = OrderedDict(sig.parameters)

        # Pop the first param since it's the self class instance
        method_parameters.popitem(False)

        for method_parameter in method_parameters.values():
            argument = self._get_argument(service, method_parameter)
            if argument is not None:
                arguments[method_parameter.name] = argument

        return arguments

    def _is_object_init(self, subject):
        """
        Check if the __init__ method for the object comes from
        the default object or has been overridden

        :param subject: The subject we want to check the __init__ for
        :type subject: mixed

        :return: Whether the __init__ method is the default on or not
        :rtype: boolean
        """
        if '__objclass__' in dir(subject.__init__) and subject.__init__.__objclass__ == object:
            return True
        return False

    def _get_argument(self, service, method_parameter):
        """
        Retrieve the argument value for the given service

        :param service: The service we need an argument for
        :param method_parameter: The parameter we need the value for
        :type service: Service
        :type method_parameter: Parameter
        :return: The argument value
        :rtype: mixed
        """
        # First check if we specified this argument for the service
        if method_parameter.name in service.arguments:
            value = service.arguments[method_parameter.name]
            # The value references an other dependency service
            if isinstance(value, Reference):
                if value.return_class == True:
                    return self.get_uninstantiated(value.name)
                else:
                    return self.get(value.name)
            return value

        # Then check if another service has this name
        if self.has_service(method_parameter.name):
            return self.get(method_parameter.name)

        # If the parameter is *args or **kwargs then we don't raise any exception
        if method_parameter.kind == Parameter.VAR_POSITIONAL or \
                method_parameter.kind == Parameter.VAR_KEYWORD:
            return None
        # If the parameter has a default value then we don't raise any exception
        if method_parameter.default is not Parameter.empty:
            return None

        self._logger.error("A required argument is not set: %s", method_parameter.name)
        raise Exception("A required argument is not set (%s)" % method_parameter.name)
