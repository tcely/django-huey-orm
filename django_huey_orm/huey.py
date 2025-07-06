from huey.api import Huey
from .storage import DjangoORMStorage


class DjangoORMHuey(Huey):
    storage_class = DjangoORMStorage


