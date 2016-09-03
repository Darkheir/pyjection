import re
import inspect

def get_service_subject_identifier(service_subject):
    """Get the snake_case identifier of the service_subject

    :param service_subject: Service subject
    :type service_subject: mixed
    :return: snake case name of the service subject
    :rtype: str
    """
    if inspect.isclass(service_subject) is True:
        subject_name = service_subject.__name__
    else:
        subject_name = service_subject.__class__.__name__
    return convert_camel_to_snake(subject_name)

def convert_camel_to_snake(value):
    """Convert string from CamelCase to snake_case

    :param value: CamelCase value
    :type value: str
    :return: snake_case converted value
    :rtype: str
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()