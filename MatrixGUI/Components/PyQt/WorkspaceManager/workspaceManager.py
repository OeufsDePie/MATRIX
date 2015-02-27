import os

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
