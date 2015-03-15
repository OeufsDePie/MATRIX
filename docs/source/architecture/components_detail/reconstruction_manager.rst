#####################
Recontruction Manager
#####################

This section describes several things about the module used to launch
the recontruction. This module is included in the project as a git
submodule and has it's own github repository (OpenMVGFeeder_).  Right
now, the reconstruciton manager has two versions (the older is the one
included in the final version of the application).

=======================================
Interface with the openMVG command line
=======================================

The reconstruction manager is simply a front end to the openMVG
command line. It is very similar with the `Picture Fetcher`_ module :
we also use the subprocess submodule from python to call directly
openMVG through the command line.

This version is pretty basic and doesn't handle many things we would
have wanted to implement like detection of new point cloud
file. That's why there is another version, but we didn't have the time
to integrate it in our last version of the application.

==================================
Recontruction Manager improvements 
==================================

In this improvement, we first added a function, ``pointCloudDetected``
able to emit a signal when a new point cloud is detected in a specific
folder (given as a parameter).

When the orchestrator creates a reconstruction manager, it creates a
new object with default atttributes :

- A list of ``.ply`` files it already has : initialize empty.
- A new signal called `newPointCloud`
- A new `QFileSystemWatcher_` initially watching nothing and that we
  connect with the pointCloudDetected (described previously) slot.

Then, when we launch a new recontruction, we call the
``launchReconstruction`` function. This function is working like in
the first version, except that every time it is called, we add the
openMVG output directory to the list of folder watched by the file
watcher. Every time a new point cloud is detected in this folder, we
copy it in the output folder used by the 3D renderer (the path is
given as a parameter).

.. _OpenMVGFeeder: https://github.com/OeufsDePie/OpenMVGFeeder
.. _Picture Fetcher:
   http://oeufsdepie.github.io/MATRIX/architecture/components_detail/picture_fetcher.html
.. _QFileSystemWatcher :
   http://pyqt.sourceforge.net/Docs/PyQt5/api/qfilesystemwatcher.html
