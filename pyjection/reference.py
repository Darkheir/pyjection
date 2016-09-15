from pyjection.helper import get_service_subject_identifier


class Reference(object):
    """
    Base class used when a service needs to register a dependency to another service
    """

    def __init__(self, name, return_class=False):
        """
        :param name: Name of the reference
        :type name: str
        :param return_class: Whether the reference is on an instance of the other service or a class
        :type return_class: bool
        """
        self._name = name
        if isinstance(name, str) is False:
            self._name = get_service_subject_identifier(name)
        self._return_class = return_class

    @property
    def name(self):
        return self._name

    @property
    def return_class(self):
        return self._return_class
