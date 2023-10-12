"""
=======
BEaTmap
=======

BEaTmap is a tool for determining the valid P/P0 range in BET isotherms.

"""

import logging as _logging

_logging.basicConfig(level=_logging.WARNING)

from . import core, io, utils, vis
from .core import run_beatmap

__version__ = "0.2"
