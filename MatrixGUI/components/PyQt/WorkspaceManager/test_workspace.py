#!/usr/bin/env python3
import os
import WorkspaceManager
from WorkspaceManager import *

wsm = WorkspaceManager()

# Test workspace creation
print("\n######################## Creating new workspaces ##########################")
wsm.new_workspace("Workspace 1", "/home/matthieu/GIT/ENSEEIHT/3A/PL_POPART/MATRIX_matthieu/MatrixGUI/Workspace_1")
wsm.new_workspace("Workspace 2", "/home/matthieu/GIT/ENSEEIHT/3A/PL_POPART/MATRIX_matthieu/MatrixGUI/Workspace_2")

# Test already existing workspace
print("\n######################## Creating a workspace that already exists ##########################")
try:
    wsm.new_workspace("Workspace 12", "/home/matthieu/GIT/ENSEEIHT/3A/PL_POPART/MATRIX_matthieu/MatrixGUI/Workspace_1")
except AssertionError as e:
    print(e)

# Test of getting current workspace
print("\n######################## Getting the current workspace ##########################")
print(wsm.current_workspace)
ws = wsm.get_current_workspace()

# Test of setting current workspace
print("\n######################## Setting the current workspace ##########################")
wsm.set_current_workspace('/home/matthieu/GIT/ENSEEIHT/3A/PL_POPART/MATRIX_matthieu/MatrixGUI/Workspace_1')
print(wsm.current_workspace)

# Test of deleting a workspace
print("\n######################## Deleting the current workspace ##########################")
wsm.delete_workspace(wsm.current_workspace)
print(wsm.current_workspace)

# Test of creating scenes
print("\n######################## Creating scenes ##########################")
wsm.set_current_workspace('/home/matthieu/GIT/ENSEEIHT/3A/PL_POPART/MATRIX_matthieu/MatrixGUI/Workspace_2')
wsm.new_scene("Première scene")
wsm.new_scene()
wsm.new_scene("Scene avec path différent", "path_différent")

# Test of creating a scene already existing
print("\n######################## Creating a scene already existing ##########################")
try:
    wsm.new_scene("Scene avec path encore différent", "path_différent")
except AssertionError as e:
    print(e)

# Test of deleting scenes
print("\n######################## Deleting scenes ##########################")
wsm.delete_scene("path_different")

# Test of deleting a non-existing scene
print("\n######################## Deleting already existing scenes ##########################")
try:
    wsm.delete_scene("path_different")
except AssertionError as e:
    print(e)
