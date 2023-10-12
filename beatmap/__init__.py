"""
=======
BEaTmap
=======

BEaTmap is a Python library for performing BET analysis!

"""

import logging as _logging

_logging.basicConfig(level=_logging.WARNING)

from . import core, io, utils, vis
from .core import run_beatmap

__version__ = "0.1.2"
