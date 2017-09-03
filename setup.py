from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os.path
import re

from setuptools import setup, find_packages

here = os.path.dirname(__file__)

with open(os.path.join(here, "README.md"), "rt") as readme_file:
    readme = readme_file.read()

with open(os.path.join(here, "src/rr/statemachine/__init__.py"), "rt") as source_file:
    version_match = re.search(r"__version__\s*=\s*(['\"])(.*)\1", source_file.read())
if version_match is None:
    raise Exception("unable to extract version from {}".format(source_file.name))
version = version_match.group(2)

setup(
    name="rr.statemachine",
    version=version,
    description="Library for creation of FSAs, Markov chains, and other discrete state machines.",
    long_description=readme,
    url="https://github.com/2xR/rr.statemachine",
    author="Rui Jorge Rei",
    author_email="rui.jorge.rei@googlemail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
)
