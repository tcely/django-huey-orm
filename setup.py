from setuptools import setup

import django_huey_orm

author = "tcely"
name = django_huey_orm.name
version = django_huey_orm.__version__

readme = open("README.md").read()

setup(
    name=name,
    version=version,
    packages=[name],
    include_package_data=True,
    url="https://github.com/{}/{}".format(author, name),
    project_urls={
        "GitHub Repo": "https://github.com/{}/{}".format(author, name),
        "Bug Tracker": "https://github.com/{}/{}/issues".format(author, name),
    },
    license="MIT",
    author="Amos Vryhof",
    author_email="avryhof@gmail.com",
    description="A module to use Django ORM for storage with huey.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="huey,django,django_huey,huey.contrib.djhuey",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=["Django", "huey"],
    python_version=">=3.8",
)
