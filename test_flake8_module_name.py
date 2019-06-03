import os
import random
import subprocess
import sys

import pytest

from flake8_module_name import ModuleNameChecker
from flake8_module_name import valid_pep8_filename


@pytest.mark.parametrize(
    "filename,result", [("module", True), ("module123", True), ("MODULE", False)]
)
def test_valid_pep8_filename(filename, result):
    assert result == valid_pep8_filename(filename)


@pytest.mark.parametrize(
    "module_name,result",
    [
        ("my_module.py", 0),
        ("my_module/__init__.py", 0),
        ("my_module/123_module.py", 0),
        ("MYMODULE/__init__.py", 1),
        ("MYMODULE.py", 1),
    ],
)
def test_ModuleNameChecker(module_name, result):
    checker = ModuleNameChecker(None, module_name)
    assert len(list(checker.run())) == result


def test_end_to_end():
    cmd = "flake8 --ignore=N999, flake8_module_name.py"
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    assert proc.returncode == 0


@pytest.fixture()
def failing_module():
    for _ in range(100):
        name = "MYMODULE{}.py".format(random.randint(0, sys.maxsize))
        if not os.path.exists(name):
            break
    else:
        pytest.skip()

    with open(name, "w") as f:
        os.utime(name, None)
    yield name
    os.remove(name)


def test_end_to_end_failing_example(failing_module):
    cmd = "pytest --flake8 {}".format(failing_module)
    proc = subprocess.Popen(cmd, shell=True)
    proc.wait()
    assert proc.returncode != 0
