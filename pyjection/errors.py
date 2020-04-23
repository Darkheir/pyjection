class PyjectionError(Exception):
    pass


class ServiceNotFoundError(PyjectionError):
    pass


class ArgumentNotFoundError(PyjectionError):
    pass
