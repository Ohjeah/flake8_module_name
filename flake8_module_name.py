import os
import re

__version__ = "0.2.0"

PATTERN = "[^0-9a-z_]"

search = re.compile(PATTERN).search


def valid_pep8_filename(fname):
    return not bool(search(fname))


class ModuleNameChecker(object):
    """Checker of PEP-8 Module Name Conventions."""

    name = "module-naming"
    code = "N999"
    version = __version__

    def __init__(self, tree, filename):
        self.filename = filename

    @property
    def template(self):
        return "{} {{}}name should be all lower case".format(self.code)

    def run(self):
        base_name = os.path.basename(self.filename)
        fn, _ = os.path.splitext(base_name)
        if fn == "__init__":
            fn = self.filename.split(os.path.sep)[-2]
            typ = "modul"
        else:
            typ = "file"
        valid = valid_pep8_filename(fn)
        if not valid:
            message = self.template.format(typ)
            yield 0, 0, message, type(self)
