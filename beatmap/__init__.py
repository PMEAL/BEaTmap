import logging
logging.basicConfig(level=logging.WARNING)

from . import utils
from . import vis
from . import io
from . import core
from .core import run_beatmap

__version__ = "0.0.1"
