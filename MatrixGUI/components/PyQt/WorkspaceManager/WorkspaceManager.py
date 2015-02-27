import os
import xml.etree.cElementTree as ET

class WorkspaceManager(object):
  '''
    Will handle all intereaction between user and modules and the working space.
    This class is responsible for managing files inside the workspace and for
    communicating any change through signal
  '''

  def setProjectPath(self, projectPath):
    '''
      Define the root path of the project
    
      projectPath -- The path
    '''
    self.projectPath = projectPath

  def pictureModelPath(self):
    '''
      Retrieve the model file that sums up every piece of information about 
      pictures on the project.
    '''
    return os.path.join(self.projectPath, "pictures.xml")

  def generateModel(self, picturesFiles):
    root = ET.Element("pictures")
    for url in picturesFiles:
      ET.SubElement(root, "picture", status="0").text = url.path() 
      ET.SubElement(root, "picture", status="1").text = url.path() 
      ET.SubElement(root, "picture", status="2").text = url.path() 
      ET.SubElement(root, "picture", status="3").text = url.path() 

    tree = ET.ElementTree(root)
    tree.write(self.pictureModelPath())
