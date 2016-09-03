from pyjection.helper import get_service_subject_identifier


class Reference(object):
    """
    Base class used when a service needs to register a dependency to another service
    """
    
    def __init__(self, name):
        self._name = name
        if isinstance(name, str) is False:
            self._name = get_service_subject_identifier(name)

    @property
    def name(self):
        return self._name
