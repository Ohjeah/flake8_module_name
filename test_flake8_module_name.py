import subprocess

import pytest

from flake8_module_name import ModuleNameChecker
from flake8_module_name import valid_pep8_filename


@pytest.mark.parametrize("filename,result", [("module", True), ("MODULE", False)])
def test_valid_pep8_filename(filename, result):
    assert result == valid_pep8_filename(filename)


@pytest.mark.parametrize("module_name,result", [("my_module.py", 0),
                                                ("my_module/__init__.py", 0),
                                                ("MYMODULE/__init__.py", 1),
                                                ("MYMODULE.py", 1),
                                                ])
def test_ModuleNameChecker(module_name, result):
    checker = ModuleNameChecker(None, module_name)
    assert len(list(checker.run())) == result


def test_end_to_end():
    cmd = "pytest --flake8 flake8_module_name.py"
    assert not bool(subprocess.Popen(cmd, shell=True).returncode)
