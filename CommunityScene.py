import pygwidgets
from pyghelpers import Scene
from constants import SCENE_B, SCENE_C, SCENE_D, oLevel2Station, oLevel3Station, AQUA
import random



class CommunityScene(Scene):
    COMMUNITIES = {'Community': ''}
    def __init__(self, window, oLevel2Station, oLevel3Station):
        self.window = window
        self.communityName = ''
        self.infoGath = {}

        # Randomly generate community data
        self.numEVs = random.randint(50, 500)  # Random number of EVs served by the community
        self.level2EVs = random.randint(0, self.numEVs)  # Random split between Level 2 and Level 3 EVs
        self.level3EVs = self.numEVs - self.level2EVs

        # Initialize UI elements here
        self.titleText = pygwidgets.DisplayText(window, (50, 50), '', fontSize=36, justified='center')
        self.level2Car = pygwidgets.DisplayText(window, (50, 100), f'Level 2 EVs: {self.level2EVs}', fontSize=24)
        self.level3Car = pygwidgets.DisplayText(window, (50, 150), f'Level 3 EVs: {self.level3EVs}', fontSize=24)

        self.level2Station = oLevel2Station.number_charger()
        self.level2Display = pygwidgets.DisplayText(window, (250, 100), f'Level 2 stations: {self.level2Station}', fontSize=24)

        self.level3Station = oLevel3Station.number_charger()
        self.level3Display = pygwidgets.DisplayText(window, (250, 150), f'Level 3 stations: {self.level3Station}', fontSize=24)

        self.simButton = pygwidgets.TextButton(window, (150, 200), 'Stimulate Charging')

        self.finishButton = pygwidgets.TextButton(window, (350, 0), 'See Results')

    def receive(self, receiveID, info):
      if receiveID == 'Community': # Receive the user's name from the main scene
        if info not in self.COMMUNITIES:  # Check if the community has changed
          self.communityName = info  # Update the current community name
          # Reset and recalculate values for the new community
          self.numEVs = random.randint(50, 500)
          self.level2EVs = random.randint(0, self.numEVs)
          self.level3EVs = self.numEVs - self.level2EVs
          # Update UI elements with new values
          self.titleText.setValue(f'{self.communityName}: {self.numEVs} EVs')
          self.level2Car.setValue(f'Level 2 EVs: {self.level2EVs}')
          self.level3Car.setValue(f'Level 3 EVs: {self.level3EVs}')
        else:
          self.communityName = info 
          self.numEVs = self.COMMUNITIES[f"{info}"]['Level 2 Evs'] + self.COMMUNITIES[f"{info}"]['Level 3 Evs']
          self.level2EVs = self.COMMUNITIES[f"{info}"]['Level 2 Evs']
          self.level3EVs = self.COMMUNITIES[f"{info}"]['Level 3 Evs']
          self.titleText.setValue(f'{self.communityName}: {self.numEVs} EVs')
          self.level2Car.setValue(f'Level 2 EVs: {self.level2EVs}')
          self.level3Car.setValue(f'Level 3 EVs: {self.level3EVs}')

    def getSceneKey(self):
      return SCENE_B
  
    def handleInputs(self, eventsList, keyPressedList):
        for event in eventsList:

          if self.simButton.handleEvent(event):
              self.send(SCENE_C,'info', self.infoGath) 
              self.goToScene(SCENE_C)
          
          if self.finishButton.handleEvent(event):
              self.send(SCENE_D,'info', self.infoGath) 
              self.COMMUNITIES.update({f'{self.communityName}' : {'Level 2 Evs': self.infoGath['Level 2 Evs'], 'Level 3 Evs': self.infoGath['Level 3 Evs'], 'Level 2 Stations': self.infoGath['Level 2 Stations'], 'Level 3 Stations': self.infoGath['Level 3 Stations']}})
              self.goToScene(SCENE_D)

    def update(self):
        self.titleText = pygwidgets.DisplayText(self.window, (50, 50), f'{self.communityName}: {self.numEVs} EVs', fontSize=36, justified='center')
        self.level3Display = pygwidgets.DisplayText(self.window, (250, 150), f'Level 3 stations: {self.level3Station}', fontSize=24)
      
        self.infoGath['Community'] = self.communityName
        self.infoGath['Level 2 Evs'] = self.level2EVs
        self.infoGath['Level 3 Evs'] = self.level3EVs
        self.infoGath['Level 2 Stations'] = self.level2Station
        self.infoGath['Level 3 Stations'] = self.level3Station
        self.infoGath['Level 2 Capacity'] = oLevel2Station.get_total_capacity() 
        self.infoGath['Level 3 Capacity'] = oLevel3Station.get_total_capacity()
        
 

    def draw(self):
        self.window.fill(AQUA)  
        self.titleText.draw()  # Draw the community name and number of EVs
        self.level2Car.draw()  # Draw Level 2 EVs info
        self.level3Car.draw()  # Draw Level 3 EVs info
        self.level2Display.draw()
        self.level3Display.draw()
        self.finishButton.draw()
        self.simButton.draw()
