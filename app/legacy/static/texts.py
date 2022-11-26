intro = r"""
Brunauer–Emmett–Teller (BET) theory describes the physical adsorption of a
gas or vapour onto a solid surface. It can be thought of as an extension of
the Langmuir adsorption isotherm to multilayer adsorption, where each layer
of adsorbed molecules is described by the Langmuir equation [1]. BET theory is
commonly used to determine the specific surface area of porous materials [2].
A linear form the BET equation is shown below:

$$
\frac{p}{n(p_o - p)} = \frac{c-1}{n_m c}\frac{p}{p_o} + \frac{1}{n_m c}
$$

Analysis of adsorption isotherms by BET theory is easily done, but can provide
misleading answers. BET theory was originally developed using isothermal
adsorption data over the relative pressure range of 0.05 to 0.35, and required
several assumptions, some more reasonable than others, and some are impossible
to fulfill.

### BET theory assumptions
* The surface is homogeneous (energy of adsorption at all surface sites is the same).
* Molecules only interact with molecules in adjacent layers.
* There is no limitation on the thickness of the monolayer.
* The energy of adsorption for the first layer, E1, is higher than the energy
    of adsorption for all other layers. Energy of adsorption in forming the
    multilayer is equal to the energy of condensation, EL.
* Interactions between adsorbed molecules in the same layer are neglected.
* The second and further layers begin forming before the monolayer is completed.

An understanding of, or at least a regard for, the assumptions of BET theory is
necessary to produce a specific surface area answer that is as accurate and
repeatable. Surface homogeneity is impossible to insure, the failure of BET
theory to describe isothermal adsorption below 5% relative pressure is
attributed to the surface homogeneity. The internal surface area of porous
materials clearly limits monolayer thickness, a fact that becomes more
significant as pore size decreases. And, inter/ intralayer interaction
between adsorbed molecules is unavoidable. Only the assumption that subsequent
layers form before the monolayer is complete is realistic.

Rouquerol et al have proposed a set of criteria to select the relative pressure
range of an isotherm where experimentally observed adsorption follows the
assumptions made by BET theory, to the degree that a repeatable result is
insured [3]. Additionally, two consistency checks have been put forth, to
confirm that the monolayer amount determined from the experimental data falls
in the same range of relative pressures from which it was produced.

### BET theory checks
* The BET constant must be positive (y-intercept of the BET plot’s line of best
    fit must be positive).
* The term n(P-Po) must increase as P/Po increases [2].

### Consistency checks
* The calculated monolayer adsorbed amount, nm, must fall in the relative
    pressure range used in BET analysis.
* After setting n = nm and C to the value of C found in BET analysis and
    solving the BET equation for P/Po, the P/Po calculated should agree with the
    P/Po corresponding to nm within 10%.

Despite the work of Rouquerol et al there is no accepted set of best practices
for performing and reporting BET analysis. Some researchers select linear
regions of the isotherm data, others use the traditional range of 0.05 to 0.35,
while others apply Rouquerol criteria in their analysis. In many cases
researchers confirm the results of BET analysis and justify their selection of
relative pressure range for the isotherm after the  fact, by comparing their
experimental results with modeling work.

**BEaTmap** (**B**runauer **E**mmett **a**nd **T**eller heat**map**) has been
developed as a conceptualization and visualization tool illustrating the
the portions of isothermal adsorption data that adhere to BET theory. The
selection criteria of **BEaTmap** reflect the criteria proposed by Rouquerol et
al, and a 5th parameter, the minimum number of data points considered in BET
analysis, has been included.

The graphical representation of how BET theory applies to an isotherm,
facilitated by **BEaTmap**, serves to provide more comprehensive BET analysis
and a more rigorous specific surface area answer than conventional BET analysis
tools.
"""

getting_started = r"""
To analyze your adsorption data using BEaTmap, here's how the workflow works:

1. Save your data in a `csv` file, with the **first column** being
    **relative pressure** values and the **second** being the
    **adsorbed amount** in _mol per gram_.

2. Upload your data on this page and provide the cross sectional area of the
    adsorbate in _square Angstrom per molecule_.

3. From the **Sidebar**, click on **BEaTmap Analysis**. Select the underlying
    assumptions and calculation criterion. The criteria are reflected in the
    specific surface area heatmap.

4. For additional tables and figures click over to the
    **Supplemental Analysis** page in the **Sidebar**.
"""

intro_sidebar = r"""
**BEaTmap** (**B**runauer **E**mmett **a**nd **T**eller heat**map**) is a
scientific (web)app for performing BET analysis on isotherm adsorption data.
"""

checks = [
    r"""𝑛(𝑃𝑜−𝑃) must increase as relative pressure increases.""",
    r"""Force y-intercept of BET equation to be positive (i.e. positive BET
    constant, C)""",
    r"""The monolayer adsorbed amount, 𝑛𝑚, must fall within the range of
    adsorbed amounts of the relative pressure interval.""",
    r"""Set 𝑛 equal to 𝑛𝑚 in the BET equation and solve for relative pressure.
    This relative pressure is then compared to the experimental relative
    pressure corresponding to monolayer completion and must agree within 10%.""",
    r"""Set a minimum number of data points required for a relative pressure
    range to be considered valid.""",
]

upload_instruction = r"""
Save your data in a `csv` file, with the first column being relative pressure
values and the second being the adsorbed amount in mol per gram.
Upload the `csv` file using the drag and drop widget, or manually browse from
your computer.
"""

area_instruction = r"""
Enter the cross sectional area of the adsorbate in square Angstrom per
molecule.
"""

ssa_instruction = r"""
The specific surface area values that result from BET analysis can be
visualized as a heatmap, where every cell represents a relative pressure range.
The gradient of each cell corresponds to the specific surface area of that
relative pressure range.
"""

err_instruction = r"""
The error values that result from BET analysis can be visualized
as a heatmap, where every cell represents a relative pressure range. The
gradient of each cell corresponds to the average error between an experimental
data point and the BET isotherm for that relative pressure range.
"""

bet_plot_instruction = r"""
The BET plot for the specific answer value displayed above.
"""

bet_combo_instruction = r"""
The BET plots for valid relative pressure range with the highest and lowest
error. As criteria are relaxed the difference between the two becomes more
apparent, demonstrating the importance of selection criteria.
"""

iso_combo_instruction = r"""
Experimental isotherm data and the BET model isotherm corresponding to the
specific surface area value displayed above. Data points used in the BET
analysis are highlighted. The point at which monolayer coverage occurs is
where n/nm = 1.
"""


references = r"""

1. Brunauer, S. et al, **BET Equation.** _Adsorption of Gases in
    Multimolecular Layers. Journal of the American Chemical Society (1938):
    309–319._

2. S. J. Gregg und K. S. W. Sing: **Adsorption, Surface Area and Porosity**
    2nd ed. _Academic Press, London, New York 1982_.

3. Rouquerol, J., P. Llewellyn, and F. Rouquerol. **Is the BET equation
    applicable to microporous adsorbents.** _Stud. Surf. Sci. Catal 160.07 (2007):
    49-56._
"""
