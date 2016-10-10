import inspect


class Service(object):
    """
    A service represents a class that the dependency injector can instantiate when asked.

    After the service has been declared, its arguments might be specified
    using the methods add_argument or add_arguments.
    The argument value can be:
        * A raw value that will be injected as it is when instantiating the service
        * A reference to another service. This reference service will be instantiated
        before being injected during the service instantiation
    """

    def __init__(self, subject):
        self._subject = subject
        self._arguments = dict()
        self._is_singleton = False
        self._type = "instance"
        if inspect.isclass(subject) is True:
            self._type = "class"            

    @property
    def type(self):
        return self._type

    @property
    def is_singleton(self):
        """
        Get whether this service is a Singleton or not
        """
        return self._is_singleton

    @is_singleton.setter
    def is_singleton(self, value):
        """
        Set whether this service is a Singleton or not
        """
        self._is_singleton = value

    @property
    def subject(self):
        """
        Subject of this service

        The subject might be a class that will be instantiated
        or an instance that just will be returned
        """
        return self._subject

    @property
    def arguments(self):
        """
        Arguments of this service

        :rtype: dict
        """
        return self._arguments

    def add_argument(self, name, value):
        """
        Add an argument to this service

        The argument value can be a reference to another service.
        In this case the reference service will be instantiated
        before being injected in this service

        :param name: Name of the argument to add
        :param value: Value to assign to the argument
        :type name: string
        :type value: mixed
        :return: The service
        :rtype: Service
        """
        self._arguments[name] = value
        return self

    def add_arguments(self, **kwargs):
        """
        Add several arguments to this service.
        """
        self._arguments.update(kwargs)
        return self
