#####################
3D Rendering Module
#####################

The 3D renderer is C++ module that has to be compile as a QML plugin
to be used in the application. The communication between the module
and the orchestrator can only be made through QML. To display openGL
under QML, we used the QML `scene graph`_.

=========================================
openGL implementation and ``.ply`` reader
=========================================

The C++ code for the openGL implementation is based on this tutorial_
. There are many differences as we had to use this module in a Qt
context : we had to convert every C++ openGL function in Qt openGL
functions.

Those are really often the same function, only the name changes. Only
`Buffer Object`_ and `Vertex Array Object`_ are different since they
are Qt object that we have to create before using them.

The ``.ply`` reader can be found in an old commit made in the `openMVG
repository`_. This reader is the one initializing the position and
color buffers of the renderer.

When a point cloud has been read by the reader, we initialize a list
of camera coordinates simply by reading the end of the position buffer
(because cameras are found at the end of the ply file). We then
initialize the default camera to the first camera : that's the default
point of view used for the renderer. We can switch this point of view,
in the camera list order, simply by calling the ``nextCam`` function.
The renderer is still pretty basic, but what is interesting here is
the conversion between the C++ openGL implementation to a Qt
implementation. We then describe how to use this renderer as a QML
plugin. The ``pathply`` attribute and the ``nextCam`` function are two
good examples of interactions between QML and the plugin, and are two
ways of communicating (by setting attributes directly from QML, or by
calling a C++ function also directly from QML).

=========================================
The QML Plugin
=========================================

To create a new QML plugin, we followed the QT documentation_. The
plugin is in the ``PointCloud.cpp`` file as a new class extending
QQmlExtensionPlugin_.  As said before, we used the QML scene graph to
display openGL under QML. As explained in the tutorial, we had to
separate the PointCloud, which lives in the GUI thread, and the
PointCloudRenderer, which lives in the rendering thread.  When the
``beforeRendering`` signal from the window is emitted , at the start
of every frame before the window rendering, any OpenGL draw calls that
are made as a response to this signal will stack under the Qt Quick
items. We then simply connect the ``beforeRendering`` signal to the
renderer paint function to paint the PointCloud.

==========================================
Communication between QML and the plugin
==========================================

With our plugin, you can either communicate by directly calling C++
function from QML, or by dynamically setting attribute in QML. We
implemented both ways of communication :

- You can set in the QML PointCloud object a path to a ply file used
  for the rendering. The communication is not made directly from QML
  to the renderer, you have to use the PointCloud to communicate.  To
  set the ply path, we added a setter and a getter, and also a `Qt
  property`_ in order to make QML aware on how to set and get the
  attribute.
- You can call directly from QML the nextCam function. To do that, you
  also have to go through the point cloud object and not directly call
  the renderer function. You have to add a `Qt invokable`_ function
  which calls the renderer function.

Note that you really have to be aware of the whole logic behind the
scene graph in order to synchronize everything. You especially have to
use the QQuickItem function like ``sync`` to be able to stack the
openGL calls under the Qt Quick item.

.. _Qt invokable: https://qt-project.org/search/tag/q_invokable
.. _Qt property : http://doc.qt.io/qt-5/properties.html
.. _documentation : http://developer.ubuntu.com/api/qml/sdk-14.10/QtQml.qtqml-modules-cppplugins/
.. _QQmlExtensionPlugin : http://doc.qt.io/qt-5/qqmlextensionplugin.html
.. _scene graph : http://doc.qt.io/qt-5/qtquick-scenegraph-openglunderqml-example.html
.. _Buffer Object : doc.qt.io/qt-5/qopenglbuffer.html
.. _Vertex Array Object : http://doc.qt.io/qt-5/qopenglvertexarrayobject.html
.. _tutorial : https://www.opengl.org/wiki/Tutorial2:_VAOs,_VBOs,_Vertex_and_Fragment_Shaders_%28C_/_SDL%29
.. _openMVG repository : https://github.com/openMVG/openMVG/
