##################
Code Documentation
##################

Here comes the semi-automatically generated code documentation.

For now the commands I used are :

.. code-block:: bash

   sphinx-apidoc -f -o source/code ../MatrixGUI
   sphinx-apidoc -f -o source/code/Python ../MatrixGUI/Components/Python
   sphinx-apidoc -f -o source/code/PyQt ../MatrixGUI/Components/PyQt

There are still some problems since the Google docstring syntax is not recognized.
If I try to use ``napoleon`` (see http://sphinx-doc.org/ext/napoleon.html#module-sphinx.ext.napoleon).
I have that error :

.. code-block:: python

   Could not import extension sphinx.ext.napoleon (exception: No module named 'sphinx.ext.napoleon')

.. note::

   Problem solved by updating Sphinx from 1.2.3 to 1.3 with ::

      sudo pip install sphinx --upgrade

   But still some errors and warnings to deal with

.. toctree::
   :maxdepth: 2
   :glob:

   code/modules
   code/Python/modules
   code/PyQt/modules
