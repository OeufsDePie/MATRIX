*****************
Workspace Manager
*****************

The WorkspaceManager package is made of 4 different classes :

* WorkspaceManager
* DirectorySpace
* Workspace
* Scene

The WorkspaceManager class is serving as an interface between the
ochestrator and the effective workspaces and scenes.

Internally the three other classes (DirectorySpace, Workspace and
Scene) handle the creation, manipulation and destruction of workspaces
and scenes.  In order to make a DRY (Don't Repeat Yourself) code,
every feature shared between workspaces and scenes is in the parent
class DirectorySpace.  You have a simple class diagram of the
workspaces and scenes in the figure below :

.. image:: /../img/WMClassDiagram.*
   :width: 100%
   :align: center

.. attention::

   Normally, the core features of workspaces and scenes were tested
   many times and are stable.  However, during the last two days
   before the demo, some important features needed to interact with
   external modules (pictureManager, reconstructionManager, ...) were
   added without the time to do meticulous testing.  Thus it is
   possible that some bugs occur while manipulating scenes in the
   application.  But we are confident that such bugs might be easily
   corrected.
