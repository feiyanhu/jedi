import sys
if sys.hexversion < 0x02070000:
    import unittest2 as unittest
else:
    import unittest
import os
from os.path import abspath, dirname
import functools

import jedi


test_dir = dirname(abspath(__file__))
root_dir = dirname(test_dir)


sample_int = 1  # This is used in completion/imports.py


class TestBase(unittest.TestCase):
    def get_script(self, src, pos=(None, None), path=None):
        return jedi.Script(src, pos[0], pos[1], path)

    def __getattr__(self, name):
        """Allow access to all the Jedi methods with a simplified interface."""
        if not hasattr(jedi.Script, name):
            raise AttributeError("Don't use getattr on this without Jedi methods")
        def action(*args, **kwargs):
            script = self.get_script(*args, **kwargs)
            return getattr(script, name)()
        return action


def cwd_at(path):
    """
    Decorator to run function at `path`.

    :type path: str
    :arg  path: relative path from repository root (e.g., ``'jedi'``).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwds):
            try:
                oldcwd = os.getcwd()
                repo_root = os.path.dirname(test_dir)
                os.chdir(os.path.join(repo_root, path))
                return func(*args, **kwds)
            finally:
                os.chdir(oldcwd)
        return wrapper
    return decorator
