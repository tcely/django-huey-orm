[![PyPI version](http://img.shields.io/pypi/v/huey-django-orm.svg?style=flat-square)](https://pypi.python.org/pypi/huey-django-orm)
[![license](http://img.shields.io/pypi/l/huey-django-orm.svg?style=flat-square)](https://pypi.python.org/pypi/huey-django-orm)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg?style=flat-square)](https://paypal.me/avryhof?country.x=US&locale.x=en_US)

django-huey-orm
=
A module to use [`Django`](https://pypi.org/project/Django/) ORM for storage with [huey](https://pypi.org/project/huey/)

This project originally started because I wanted to just update [`huey-pg`](https://pypi.org/project/huey-pg/). That
proved to be more of a full rewrite than just an update.

Anyway, I didn't want to use `SqliteHuey`, or `FileHuey`, since I already have a perfectly good data store in my Django
project.

So, I took a copy of `SqliteHuey`, and re-implemented the class functionality using Django ORM.

Huey doesn't do anything too crazy, so it should work with any database backend supported by Django. We also don't use
any non-standard Django stuff, so it should work with any modern Django version.

## Installation

Install with pip

```bash
pip install huey-django-orm
```

### settings.py

Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    "...",
    "django_huey_orm",
    "...",
]
```

Configure Huey to use DjangoORMHuey

```python
from django_huey_orm import DjangoORMHuey

HUEY = DjangoORMHuey()
```

or if you need other options

```python
HUEY = {
    "...": "...",
    'huey_class': 'django_huey_orm.DjangoORMHuey',
    "......": "...",
}
```

### Run Migrations

```bash
python3 manage.py migrate django_huey_orm
```

That's it!  Now you can use Huey just like you normally would.

## Admin

Since this project is specific to Django, and will likely never be used without it, you get a few Django goodies rolled
right in.

* Each Model has a ModelAdmin
* There is an auto_now_add field in each model so we can see when an object was created within the admin
* Ordering is defined at the model level, so objects will appear in the admin in the same way they will be processed.
