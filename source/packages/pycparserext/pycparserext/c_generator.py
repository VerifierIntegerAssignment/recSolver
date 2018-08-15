from warnings import warn
warn("pycparserext.c_generator is deprecated. Please use pycparser.c_generator "
        "directly.", DeprecationWarning)

from pycparser1.c_generator import *  # noqa
