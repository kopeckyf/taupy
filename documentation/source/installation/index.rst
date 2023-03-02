Installation
************

Installation via pip
====================

taupy is distributed on PyPi, the Python Package Index. To install it, run

.. code-block:: 

   pip install taupy

Then, you can import :py:obj:`taupy` to a Python session. 

.. code:: python

    from taupy import *
    
Known installation issues
=========================

:py:mod:`taupy` is written in pure Python and no installation problems should 
occur for :py:mod:`taupy` itself, provided that Pyton 3.9 or newer is used.

There are some known problems installing dependencies that :py:mod:`taupy` relies
on. These can usually be solved by installing these packages from a different source
then via pip.

On Windows
^^^^^^^^^^

- Prior to version 0.5, :py:mod:`taupy` relied on :py:mod:`iteration-utilities`. 
  This package implements functions in pure C, and its source code must be compiled
  before it can be used in Python. Unfortunately the 
  package became unmaintained around Python 3.10 and no pre-compiled wheel 
  packages were available. Windows users who use Python 3.10 or newer and 
  :py:mod:`taupy` 0.4 or older are particularly affected by this, as they need
  to install Microsoft's Visual C++ Build Tools in order to compile the C code.

  As of version 0.5, :py:mod:`taupy` no longer depends on :py:mod:`iteration-utilities`
  but uses :py:mod:`more-itertools` for all non-standard combinatorial tasks.
  :py:mod:`taupy` version 0.4 or older can be used with Python 3.9 on Windows 
  without installing additional build tools.

On Mac OS
^^^^^^^^^

- No wheels are provided for :py:mod:`scipy` on the ARM version of Mac OS 11 via
  pip. On ARM Macs (“Apple Silicon M1/M2”) that run Mac OS 11, :py:mod:`scipy` 
  needs to be pre-installed via conda before :py:mod:`taupy` can be installed
  via pip. This issue can also be resolved by upgrading to a newer version of 
  Mac OS.
