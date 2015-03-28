

class Reference(object):
    """
    Base class used when a service needs to register a dependency
    to another service
    """
    
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
