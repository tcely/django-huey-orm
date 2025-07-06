import logging
from huey.api import Huey
from .storage import DjangoORMStorage

logger = logging.getLogger(__name__)

name = "django-huey-orm"
__version__ = "0.0.1"

prefix = "django_huey_orm"


class DjangoORMHuey(Huey):
    storage_class = DjangoORMStorage


