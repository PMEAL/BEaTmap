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

from ._figures import experimental_data_plot
from ._figures import ssa_heatmap
from ._figures import err_heatmap
from ._figures import bet_combo_plot
from ._figures import bet_iso_combo_plot
from ._settables import ascii_tables
from ._settables import dataframe_tables
