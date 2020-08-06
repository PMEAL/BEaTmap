intro = r"""
Brunauer–Emmett–Teller (BET) theory describes the physical adsorption of a
gas or vapour onto a solid surface. It can be thought of as an extension of
the Langmuir adsorption isotherm to multilayer adsoption, where each layer
of adsorbed molecules is described by the Langmuir equation. BET theory is
commonly used to determine the specific surface area of porous materials [1].

$$
\frac{p}{n(p_o - p)} = \frac{c-1}{n_m c}\frac{p}{p_o} + \frac{1}{n_m c}
$$

Analysis of adsorption isotherms by BET theory is easily done, but can provide
misleading answers. A paper by Roquerol et al describes five criteria that can
be used to determine which relative pressure ranges of an isotherm follow the
assumptions of BET Theory [2].

**BEaTmap** (**B**runauer **E**mmett **a**nd **T**eller heat**map**) has been
developed as a  tool, allowing the user to quickly and easily get a graphical
representation of how BET theory applies to an experimental adsoption isotherm
and provide a more rigorous specific surface area answer.

This web app is an implementation of BEaTmap. First isotherm data must be
imported in the form of a `csv` file with the first column being relative
pressure values and the second being specific amount of adsorbed molecules in
mol per gram. Cross sectional area of the adsorbate must be provided in square
Angstrom per molecule.
"""

intro_sidebar = r"""
**BEaTmap** (**B**runauer **E**mmett **a**nd **T**eller heat**map**) is a
scientific (web)app for performing BET analysis on isotherm adsorption data.
"""

checks = [
    r"""𝑛(𝑃𝑜−𝑃) must increase as relative pressure inceases.""",
    r"""Force y-intercept of BET equation to be positive (i.e. positive BET
    constant, C)""",
    r"""The monolayer adsorbed amount, 𝑛𝑚, must fall within the range of
    adsorbed amounts of the relative pressure interval.""",
    r"""Set 𝑛 equal to 𝑛𝑚 in the BET equation and solve for relative pressure.
    This realtive pressure is then compared to the experimental relative
    pressure corresopnding to monolayer completion and must agree within 10%.""",
    r"""Set a minimum number of data points required for a relative pressure
    range to be considered valid."""
]
