###########################
Building that Documentation
###########################

The objective is to have an easily maintainable and yet simple and powerful documentation.
For all these reasons we chose `Sphinx <http://sphinx-doc.org/index.html>`_.
Sphinx has many benefits :

* A simple syntax (`rST <http://fr.wikipedia.org/wiki/ReStructuredText>`_)
* Provides a simple navigation
* Manages source code blocks
* Manages source code doc comments
* Manages images
* Manages mathematics
* Manages LaTeX compilation

You will find an introduction to rST syntaxe here :
http://sphinx-doc.org/rest.html

*******************
Sphinx Installation
*******************

You can find all the details here : http://sphinx-doc.org/install.html.
The simplest way is to use Python package manager (`pip <https://pip.pypa.io/en/latest/>`_) :

.. code-block:: bash

   $ sudo pip install sphinx

.. attention::
   
   If you use some Ubuntu derived distribution,
   you might need to use ``pip3`` instead of ``pip``.


****************************
Initialize the documentation
****************************

Sources of the documentation will reside in the ``docs`` folder.
Use the ``sphinx-quickstart`` command to start the documentation :

.. code-block:: bash

   $ mkdir docs
   $ cd docs/
   $ sphinx-quickstart

The default configuration is almost ok but we need to change some answers :

.. code-block:: rst

   > Separate source and build directories (y/n) [n]: y
   > autodoc: automatically insert docstrings from modules (y/n) [n]: y
   > mathjax: include math, rendered in the browser by MathJax (y/n) [n]: y

At the end of the script, Sphinx configuration has been initialized.
It has setup 2 folders : ``build`` and ``source``.
It also created a ``Makefile`` allowing to easily build the doc with commands such as :

.. code-block:: bash
   
   $ make html

*************************************
Configuration of Sphinx documentation
*************************************

The ``sphinx-quickstart`` script generated files allowing us to configure Sphinx.
Here are some additional information to setup your documentation.

Host your documentation on Github
=================================

If you have a `Github <https://github.com/>`_ repository you can host your documentation
on the Github pages of your repository.
See https://help.github.com/articles/what-are-github-pages/
for more explanations on it.

To activate the Github pages of your repository you only have to
create a new branch called ``gh-pages`` and to push it on origin.

.. code-block:: guess

   $ git checkout --orphan gh-pages
   $ git rm -rf .
   $ echo "My page" > index.html
   $ git add index.html
   $ git commit -am "Premier commit sur les pages Github"
   $ git push origin gh-pages -u

Configure HTML build
====================

In practice we need to build into the ``gh-pages`` branch.
But it is not immediatly possible since we are not ``gh-pages``
branch when compiling.

The easiest solution according to me is to have 2 folders.
One with the standard repository,
and the other one with only the ``gh-pages`` branch
(so it is lightweight) of the same repository.
Then you only have to configure your Sphinx build so that
it builds into the folder containing the repository
on the ``gh-pages`` branch.

Example for creating the second folder :

.. code-block:: guess

   $ pwd
   /home/......../MATRIX
   $ cd ../
   $ mkdir MATRIX_gh-pages
   $ cd MATRIX_gh-pages/
   $ git clone -b gh-pages --single-branch git@github.com:mpizenberg/MATRIX.git .

Now we just need to modify the make file ``MATRIX/docs/Makefile`` :

.. code-block:: guess

   BUILDDIR = ../../MATRIX_gh-pages

   html:
      $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)

Use the theme rTD (readTheDocs)
===============================

You only need to install the theme with pip.

.. code-block:: guess

   $ sudo pip install sphinx_rtd_theme

Then in the file ``conf.py`` :

.. code-block:: guess

   import sphinx_rtd_theme
   html_theme = "sphinx_rtd_theme"
   html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

Once it is installed, there is one last manipulation.
You have to add an empty file entitled ``.nojekyll``
in the ``gh-pages`` branch.
Otherwise Github will ignore folders starting with `_`.
It would be a problem since the folder ``_static`` contains
CSS styles and images needed for the theme.
