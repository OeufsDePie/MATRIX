## Launch the application

We haven't created a makefile yet to automatically build the whole
application in one command. Which is why you have to manually compile
every modules. Once this is done, you can launch the application by
typing in the MatrixGUI folder:

```
python3 orchestrator.py
```

The application was running perfectly under Linux Ubuntu 12.04, 14.04,
14.10 and Manjaro (based on archlinux) with correct dependencies
installed (as described bellow).

## Depends

The application core depends on :
* python >= 3.0 (we all used python 3.4)
* Qt >= 5.4 (we used Qt 5.4.0 and 5.4.1)
* PyQt5 (debian package python3-pyqt5)
* PyQt5 (debian package python3-pyqt5.qtquick)
* libgl (we used 10.3.2)
* libglu (we used 9.0.0-2)
* libglm-dev (we used 0.9.5.1-1)
* libimage-exiftool-perl (we used 9.46-1)
* gphoto2 (we used 2.5.4)
* PyExifTool (python module) (0.1)
* PyOpenGL (python module) (this dependency is optionnal, if you don't
  want to use it simply comment the OpenGL import in the
  `orchestrator.py` file; but this import might solve some OpenGL
  issues)


*Note : to install python packages, use pip3 (`sudo apt-get install
 python3-pip`)*

## Building

Make sure you have cloned every submodule of our application when
cloning the main repository (by using git clone --recursive
...). Otherwise, simply try:

```
git submodule update --init --recursive
```

Go to the 3D rendering module folder and compile it :

```
cd MATRIX/MatrixGUI/Components/QML/3dRendering/
qmake && make && make clean
```

