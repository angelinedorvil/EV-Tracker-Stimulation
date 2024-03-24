# MainMenuScene.py
import pygwidgets
from pyghelpers import Scene
from constants import SCENE_A, SCENE_B, LIGHT_GRAY, GREEN


class MainMenuScene(Scene):
    COMMUNITIES = ['Bellview', 'Rivertown', 'Greendale']
  
    def __init__(self, window):
      self.window = window
      self.messageText = pygwidgets.DisplayText(window, (50, 50), 'LightningPower EV Data', fontSize=36, justified='center', textColor=GREEN)
      self.messageText2 = pygwidgets.DisplayText(window, (10, 130), 'Communities:', fontSize=20, justified='left')
      
      self.communityButtons = []
      startY = 150
      for community in self.COMMUNITIES:
          button = pygwidgets.TextButton(window, (100, startY), community)
          self.communityButtons.append((community, button))
          startY += 50 

    def getSceneKey(self):
      return SCENE_A   
  
    def handleInputs(self, eventsList, keyPressedList):
      for event in eventsList:
          for communityName, button in self.communityButtons:
            if button.handleEvent(event):
                print(f"{communityName} button was clicked")
                self.send(SCENE_B,'Community', f'{communityName}') # Send the community name to all the other scenes
                self.send(SCENE_B,'allCommunities', f'{self.COMMUNITIES}')
                self.goToScene(SCENE_B)
  
    def update(self):
      pass  
  
    def draw(self):
      self.window.fill(LIGHT_GRAY)  
      self.messageText.draw()
      self.messageText2.draw()
      for _, button in self.communityButtons:
        button.draw()