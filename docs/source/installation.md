# Installation

BEaTmap depends heavily on the Scipy Stack. The best way to get a fully functioning environment is to install the [Anaconda Python distribution](https://www.anaconda.com/download/). Be sure to get the **Python 3.9+ version**.

Once you've installed the Anaconda distribution (or the Python distribution of your choice), type and enter the following in a terminal (on Unix-based machines) or a command prompt (on Windows):

    pip install beatmap

Note that on Unix-based machines, `conda` is usually automatically initialized in the terminal. On Windows, you should have a shortcut to the "Anaconda Prompt" in the start menu, which is basically a command prompt initialized with `conda`.

Once initialized, the terminal points to the `base` environment. While you can install BEaTmap in the `base` environment, it is recommended that you create a new environment to avoid accidentally breaking your `base` environment.

If you think you may be interested in contributing to BEaTmap and wish to both *use* and *edit* the source code, then you should clone the [repository](https://github.com/PMEAL/beatmap) to your local machine, and install it using the following `pip` command:

    pip install -e path/to/beatmap/root/folder

For information about contributing, refer to the [contributors guide](https://github.com/PMEAL/beatmap/blob/main/CONTRIBUTING.md).
