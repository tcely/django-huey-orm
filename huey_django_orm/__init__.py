name = "django-huey-orm"
__version__ = "0.0.1"


from huey.api import Huey
from .storage import DjangoORMStorage


class DjangoORMHuey(Huey):
    storage_class = DjangoORMStorage


