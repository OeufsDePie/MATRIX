##################
Code Documentation
##################

Here comes the semi-automatically generated code documentation.
For now the commands used are :

.. code-block:: bash

   sphinx-apidoc -f -o source/code ../MatrixGUI
   sphinx-apidoc -f -o source/code/Python ../MatrixGUI/Components/Python
   sphinx-apidoc -f -o source/code/PyQt ../MatrixGUI/Components/PyQt

.. note::

   In order to understand google docstring format you have to use ``napoleon``
   (see http://sphinx-doc.org/ext/napoleon.html#module-sphinx.ext.napoleon)
   This requires Sphinx 1.3.

.. toctree::
   :maxdepth: 2
   :glob:

   code/modules
   code/Python/modules
   code/PyQt/modules
