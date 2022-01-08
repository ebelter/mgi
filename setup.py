# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("LICENSE") as f:
    license = f.read()

tests_require = [
    "mock",
    "nose",
]

install_requires=[
    "click>=7.0",
    "flask",
    "flask-migrate",
    "flask-sqlalchemy",
    "Jinja2>=3.0",
    "pyyaml>=5.1",
    "requests",
    "SQLAlchemy>=1.3.10",
    "tabulate",
]

setup(
    name="mgi",
    version="0.1.0",
    description="MGI Sample Management and Tools",
    author="Eddie Belter",
    author_email="ebelter@wustl.edu",
    license=license,
    url="https://github.com/hall-lab/mgi-tk.git",
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        mgi=mgi.cli:cli
        cw=cw.cli:cli
    """,
    setup_requires=["pytest-runner"],
    test_suite="nose.collector",
    tests_requires=tests_require,
    packages=find_packages(include=["mgi", "mgi.entity", "mgi.ref", "mgi.samples", "cw"], exclude=("tests")),
    include_package_data=True,
    package_data={"cw": ["resources/*"]},
)
