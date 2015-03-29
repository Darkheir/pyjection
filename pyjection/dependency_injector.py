from inspect import signature
from inspect import Parameter
from collections import OrderedDict
from pyjection.service import Service
from pyjection.reference import Reference


class DependencyInjector(object):

    def __init__(self):
        self._services = dict()
        self._singletons = dict()

    def register(self, identifier, service_subject):
        """
        Register a new service in the dependency injector

        This service can be :
            * A class that will be instantiated when called
            * An already instantiated instance that will be returned

        :param identifier: The identifier used to later retrieve a service instance
        :param service_subject: The class or instance
        :type identifier: string
        :type service_subject: mixed
        :return: Return the newly created service entry
        :rtype: Service
        """
        service = Service(service_subject)
        self._services[identifier] = service
        return service

    def register_singleton(self, identifier, service_subject):
        """
        Register a new singleton service in in the dependency injector

        This service can be :
            * A class that will be instantiated when called
            * An already instantiated instance that will be returned

        :param identifier: The identifier used to later retrieve a service singleton
        :param service_subject: The class or instance
        :type identifier: string
        :type service_subject: mixed
        :return: Return the newly created dependency entry
        :rtype: Service
        """
        service = Service(service_subject)
        service.is_singleton = True
        self._services[identifier] = service
        return service

    def get(self, identifier):
        """
        Instantiate and retrieve the service matching this identifier

        If the service has been self has a singleton the same service object
        will be return each time this service is asked

        :param identifier: The identifier used to later retrieve a class singleton
        :type identifier: string
        :return: The instantiated object
        :rtype: mixed
        """
        if identifier not in self._services:
            raise Exception("No service has been declared with this ID")

        service = self._services[identifier]

        if service.is_singleton is True and identifier in self._singletons:
            return self._singletons[identifier]

        instance = self._get_instance(service)

        if service.is_singleton is True:
            self._singletons[identifier] = instance

        return instance

    def has_service(self, identifier):
        """
        Check if the service matching the given identifier
        has already been declared

        :param identifier: Name of the service
        :type identifier: string
        :return: Wether or not the service exists
        :rtype: boolean
        """
        if identifier in self._services:
            return True
        return False

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

        #The subject extend object and han't overwritten its init
        # It's necessary because signature can't take the __init__ from object
        if ('__objclass__' in dir(service.subject.__init__) 
            and service.subject.__init__.__objclass__ == object):
            return arguments

        sig = signature(service.subject.__init__)
        method_parameters = OrderedDict(sig.parameters)

        #Pop the first param since it's the self class instance
        method_parameters.popitem(False)

        for method_parameter in method_parameters.values():
            argument = self._get_argument(service, method_parameter)
            if argument is not None:
                arguments[method_parameter.name] = argument

        return arguments

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
        if method_parameter.name in service.arguments:
            value = service.arguments[method_parameter.name]
            #The value references an other dependency service
            if isinstance(value, Reference):
                return self.get(value.name)
            return value

        #If the parameter has a default value then we don't raise any exception
        if method_parameter.default == Parameter.empty:
            raise Exception("A required argument is not set (%s)" % (method_parameter.name))
        return None
