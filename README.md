[![image](https://github.com/PMEAL/beatmap/workflows/Ubuntu/badge.svg)](https://github.com/PMEAL/beatmap/actions)
[![image](https://github.com/PMEAL/beatmap/workflows/macOS/badge.svg)](https://github.com/PMEAL/beatmap/actions)
[![image](https://github.com/PMEAL/beatmap/workflows/Windows/badge.svg)](https://github.com/PMEAL/beatmap/actions)<br/>
[![image](https://codecov.io/gh/PMEAL/beatmap/branch/master/graph/badge.svg)](https://codecov.io/gh/PMEAL/beatmap)
[![image](https://img.shields.io/badge/ReadTheDocs-GO-blue.svg)](http://beatmap.readthedocs.io/en/master/)
[![image](https://img.shields.io/pypi/v/beatmap.svg)](https://pypi.python.org/pypi/beatmap/)
[![image](https://img.shields.io/badge/DOI-10.21105/joss.01296-blue.svg)](https://doi.org/10.21105/joss.01296)

-----

**Cite as:**

CHANGE THIS:
> *Gostick J, Khan ZA, Tranter TG, Kok MDR, Agnaou M, Sadeghi MA, Jervis
> R.* **PoreSpy: A Python Toolkit for Quantitative Analysis of Porous Media
> Images.** Journal of Open Source Software, 2019.
> [doi:10.21105/joss.01296](https://doi.org/10.21105/joss.01296)

# What is BEaTmap?

Obtaining surface area of a porous sample from the interpretation of gas
adsorption isotherms is very widely done using the theory developed by Brunauer,
Emmett, and Teller in the 1950s.  The BET (or BEaT) theory is so commonly place
that the acronym has is synonymous with surface area.

The BET theory was derived with several assumptions, and these must be met for
the predicted surface area to be valid.

# Capabilities

BEaTmap consists of the following modules:

  - `core`: blah blah
  - `io`: blah blah
  - `utils`: blah blah
  - `vis`: blah blah

# Installation

BEaTmap depends heavily on the Scipy Stack. The best way to get a fully
functional environment is the [Anaconda
distribution](https://www.anaconda.com/download/). Be sure to get the
**Python 3.6+ version**.

Once you've installed *Conda*, you can then install BEaTmap. It is
available on the [Python Package
Index](https://pypi.org/project/beatmap/) and can be installed by typing
the following at the *conda* prompt:

    pip install beatmap

On Windows, you should have a shortcut to the "anaconda prompt" in the
Anaconda program group in the start menu. This will open a Windows
command console with access to the Python features added by *Conda*,
such as installing things via `pip`.

On Mac or Linux, you need to open a normal terminal window, then type
`source activate {env}` where you replace `{env}` with the name of the
environment you want to install BEaTmap. If you don't know what this
means, then use `source activate root`, which will install BEaTmap in
the root environment which is the default.

If you think you may be interested in contributing to BEaTmap and wish
to both *use* and *edit* the source code, then you should clone the
[repository](https://github.com/PMEAL/beatmap) to your local machine,
and install it using the following PIP command:

    pip install -e "C:\path\to\the\local\files\"

For information about contributing, refer to the [contributors
guide](https://github.com/PMEAL/beatmap/blob/master/CONTRIBUTING.md)

# Examples

The following code snippets illustrate blah blah. A set of examples
is included in this repo, and can be [browsed
here](https://github.com/PMEAL/beatmap/tree/master/examples).

## Loading a dataset

BEaTmap blah blah.

``` python
import beatmap as bt
import matplotlib.pyplot as plt
blah blah
```
<p align="center">
  <img src="https://github.com/PMEAL/porespy/raw/dev/docs/_static/fig1.png" width="50%"></img>
</p>

## Blah blah

blah blah
