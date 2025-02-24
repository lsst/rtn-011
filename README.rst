.. image:: https://img.shields.io/badge/rtn--011-lsst.io-brightgreen.svg
   :target: https://rtn-011.lsst.io
.. image:: https://github.com/rubin-observatory/rtn-011/workflows/CI/badge.svg
   :target: https://github.com/rubin-observatory/rtn-011/actions/

#######################
Plans for Early Science
#######################

RTN-011
=======

Science prior to the first annual data release is a priority for Rubin Observatory operations. This document provides the plans for enabling early science.  It is a living document that will evolve over the course of the pre-operations period. 

Links
=====

- Live drafts: https://rtn-011.lsst.io
- GitHub: https://github.com/rubin-observatory/rtn-011

Cite as
=======

This document is published on Zenodo. Cite as::

    Leanne P. Guy, Keith Bechtol, Eric Bellm, Bob Blum, Melissa L. Graham, Željko Ivezić, Robert Lupton, Phil Marshall, Colin T. Slater, Michael Strauss, Gregory Dubois-Felsmann (2023)
    Rubin Observatory Plans for an Early Science Program (5.0). Zenodo. 
    https://zenodo.org/records/10059624

Build
=====

This repository includes lsst-texmf_ as a Git submodule.
Clone this repository::

    git clone --recurse-submodules https://github.com/rubin-observatory/rtn-011

Compile the PDF::

    make

Clean built files::

    make clean

Docker 
------

Compile this document through an lsst-texmf Docker image to avoid installing LaTeX and lsst-texmf on your own computer::

    docker build --platform linux/amd64 -t rtn-011-env .
    docker run --rm -v "$(pwd)":/app rtn-011-env

Or run the included script::

    ./build.sh

Updating acronyms
-----------------

A table of the technote's acronyms and their definitions are maintained in the ``acronyms.tex`` file, which is committed as part of this repository.
To update the acronyms table in ``acronyms.tex``::

    make acronyms.tex

*Note: this command requires that this repository was cloned as a submodule.*

The acronyms discovery code scans the LaTeX source for probable acronyms.
You can ensure that certain strings aren't treated as acronyms by adding them to the `skipacronyms.txt <./skipacronyms.txt>`_ file.

The lsst-texmf_ repository centrally maintains definitions for LSST acronyms.
You can also add new acronym definitions, or override the definitions of acronyms, by editing the `myacronyms.txt <./myacronyms.txt>`_ file.

Updating lsst-texmf
-------------------

`lsst-texmf`_ includes BibTeX files, the ``lsstdoc`` class file, and acronym definitions, among other essential tooling for LSST's LaTeX documentation projects.
To update to a newer version of `lsst-texmf`_, you can update the submodule in this repository::

   git submodule update --init --recursive

Commit, then push, the updated submodule.

.. _lsst-texmf: https://github.com/lsst/lsst-texmf
