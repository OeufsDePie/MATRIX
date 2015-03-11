###############
Picture Fetcher
###############

.. _pygphoto.py: http://example.com/
.. _libgphoto2: http://gphoto.sourceforge.net/doc/api/index.html
.. _gphoto2: http://www.gphoto.org/
.. _gphoto2 command-line interface: http://www.gphoto.org/doc/manual/ref-gphoto2-cli.html
.. contents::

This module is made of a single class ``Pygphoto`` defined in the file
`pygphoto.py`_. It allows to interact with a USB camera using the
`gphoto2`_ tool. Common actions include : listing the names of the
photos present in the camera, watching for new files, downloading
photos individually etc.

Interface with the ``gphoto2`` command-line interface
*****************************************************

The module uses directly the `gphoto2 command-line interface`_ for
prototyping. It would be wiser to create a `C` module that uses the
``C`` API of gphoto2 called `libgphoto2`_ and offer a interface for all
the needed operations. This `C` module would be compiled as a shared
library and imported in Python with `ctypes
<http://docs.python.org/3/library/ctypes.html>`_.

However, the current implementation makes extended use of the
command-line interface provided by ``gphoto2``, through hardcoded calls
and output parsing.

The calls to gphoto2 are made with the `subprocess
<http://docs.python.org/3.4/library/subprocess.html>`_ Python module.

Simple calls are done like so::

  command = ["gphoto2", "--get-all-files"]
  return_code = subprocess.call(command)

When the output need to be parsed, it is necessary to use the blocking
``subprocess.check_output()`` function and to decode the binary stream
as an UTF-8 string::

  command = ["gphoto2", "--summary"]
  output_string = subprocess.check_output(command).decode("utf-8")

Active watching of the camera
*****************************

When instantiated, the ``Pygphoto`` class create a daemon thread that
actively watch for new camera connections/disconnections and pictures
creation/deletion. The two associated signals ``onCameraConnection`` and
``onContentChanged`` are the only signals emitted by ``Pygphoto``.

The ``CameraWatcher`` internal class is responsible for the active
watching. The threading is made by moving the instance of
``CameraWatcher`` to a ``QThread`` at initialisation. Using ``QThread``
allows for easy asynchronous communication with the ``CameraWatcher``'s
thread through the use of `Qt`'s signals.

**Note**: As the ``CameraWatcher`` class is internal, ``Pygphoto``
must forward every signals emitted by ``CameraWatcher`` to the
exterior. The same goes for slots connections. As a consequence, every
slot and signal of ``CameraWatcher`` is duplicated in the the parent
``Pygphoto`` class.

Camera locking
**************

The camera device can be busy for several reasons. This usually end up
throwing the following error message ::

  *** Error ***              
  An error occurred in the io-library ('Could not lock the device'): Camera is already in use.
  *** Error (-60: 'Could not lock the device') ***      

Sometimes it comes from other processes or daemons accessing the
camera. We do not do anything about them and we did not explore this
issue further. Sometimes, however, the lock comes from simultaneous
calls to ``gphoto2`` made by the application. To avoid such problems, we
use a `thread synchronization lock
<http://docs.python.org/3.4/library/threading.html#threading.Lock>`_
every time we make a call to ``gphoto2``::

  self._camera_lock = threading.Lock()
  command = [Pygphoto._GPHOTO, "--auto-detect"]
  with self._camera_lock:
      output = subprocess.check_output(command).decode("utf-8")
  # The call has returned, the lock is released
  # Continue working with output...

The lock is internal to the ``Pygphoto`` class, the only class that can
make calls to ``gphoto2``. The lock issue is thus hidden from the
exterior. It is important to note that the ``Pygphoto`` class should not
be instantiated twice, and could actually be implemented as a
singleton class.
