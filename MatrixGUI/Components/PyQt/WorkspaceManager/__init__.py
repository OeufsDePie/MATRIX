import sys
import os

# Adding the path to Python path
current_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_folder)

# Adding the path of another package (for persistence)
component_folder = os.path.dirname(os.path.dirname(current_folder))
sys.path.append(os.path.join(os.path.join(component_folder,"Python"), "Persistence"))
sys.path.append(os.path.join(component_folder, "PyQt", "PictureManager"))
