import os
import sys

py33 = sys.version_info >= (3, 3)


def import_path(fullpath):
    """ Import a file with full path specification. Allows one to
        import from anywhere, something __import__ does not do.
    """
    # http://zephyrfalcon.org/weblog/arch_d7_2002_08_31.html
    path, filename = os.path.split(fullpath)
    filename, ext = os.path.splitext(filename)
    if py33:
        from importlib import machinery
        return machinery.SourceFileLoader(
            filename, path).load_module(filename)
    else:
        from six.moves import reload_module as reload
        sys.path.append(path)
        try:
            module = __import__(filename)
            reload(module)  # Might be out of date during tests
            return module
        finally:
            del sys.path[-1]
