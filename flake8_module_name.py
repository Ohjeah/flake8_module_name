import os
import re

__version__ = "0.1.3"

PATTERN = "[^a-z_]"

search = re.compile(PATTERN).search

def valid_pep8_filename(fname):
    return not bool(search(fname))


class ModuleNameChecker(object):
    """Checker of PEP-8 Module Name Conventions."""
    name = "module-naming"
    version = __version__

    def __init__(self, tree, filename):
        self.filename = filename

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
            message = "N999 {}name should be all lower case".format(typ)
            yield 0, 0, message, type(self)
