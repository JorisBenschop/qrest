__version__ = "4.1.0"

from .resource import JSONResource  # noqa: F401
from .conf import APIConfig, ResourceConfig, BodyParameter, QueryParameter  # noqa: F401
from .conf import FileParameter  # noqa: F401
from .exception import RestClientConfigurationError  # noqa: F401
from .resource import API  # noqa: F401
