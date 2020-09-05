r"""

===============================================================================
vis
===============================================================================

.. autosummary::

    beatmap.vis.experimental_data_plot
    beatmap.vis.ssa_heatmap
    beatmap.vis.err_heatmap
    beatmap.vis.bet_combo_plot
    beatmap.vis.bet_iso_combo_plot
    beatmap.vis.ascii_tables
    beatmap.vis.dataframe_tables

.. autofunction:: index_of_value
.. autofunction:: experimental_data_plot
.. autofunction:: ssa_heatmap
.. autofunction:: err_heatmap
.. autofunction:: bet_combo_plot
.. autofunction:: bet_iso_combo_plot
.. autofunction:: ascii_tables
.. autofunction:: dataframe_tables

"""

from .figures import experimental_data_plot
from .figures import ssa_heatmap
from .figures import err_heatmap
from .figures import bet_combo_plot
from .figures import iso_combo_plot
from .settables import ascii_tables
from .settables import dataframe_tables
