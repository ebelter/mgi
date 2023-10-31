# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("LICENSE") as f:
    license = f.read()

tests_require = [
    "mock",
    "nose",
]

install_requires=[
    "Bio",
    "click>=8.0",
    "Jinja2>=3.0",
    "matplotlib",
    "numpy",
    "pandas",
    "plotnine",
    "pyyaml>=5.1",
    "tabulate",
]

setup(
    name="cig-metrics",
    version="0.1.0",
    description="CGI@MGI Metrics Scripts & Tools",
    author="Eddie Belter",
    author_email="ebelter@wustl.edu",
    license=license,
    url="https://github.com/genome/cig.git",
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        metrics=cig.metrics.cli:cli
    """,
    setup_requires=["pytest-runner"],
    test_suite="nose.collector",
    tests_requires=tests_require,
)
