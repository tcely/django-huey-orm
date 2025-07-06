import logging

from .huey import DjangoORMHuey
from .vars import NAME as name # noqa: F401
from .version import VERSION as __version__ # noqa: F401

logger = logging.getLogger(__name__)


