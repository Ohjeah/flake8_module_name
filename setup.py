import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

NAME = "flake8_module_name"
FILE = "{}.py".format(NAME)
DESCRIPTION = "A flake8 plugin for testing PEP-8 conform package and module names."
URL = "https://github.com/ohjeah/flake8_module_name"
EMAIL = "info@markusqua.de"
AUTHOR = "Markus Quade"

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, FILE)) as f:
    exec(f.read(), about)


class PublishCommand(Command):
    """Support setup.py publish."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds ...")
            rmtree(os.path.join(here, "dist"))
        except FileNotFoundError:
            pass

        self.status("Building Source and Wheel (universal) distribution...")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPi via Twine...")
        os.system("twine upload dist/*")

        sys.exit()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    py_modules=[NAME],
    install_requires=[],
    license="MIT",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    cmdclass={
        "publish": PublishCommand,
    },
    entry_points={
        "flake8.extension": ["N999 = flake8_module_name:ModuleNameChecker"],
    },
)
