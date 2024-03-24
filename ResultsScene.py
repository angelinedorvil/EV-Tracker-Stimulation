import pygwidgets
import pygame, sys
from pygame.locals import QUIT
from pyghelpers import Scene
from constants import WHITE, SCENE_D, PURPLE, SCENE_A


class ResultScene(Scene):
    def __init__(self, window):
        self.window = window
        # Initialize DisplayText objects for each result metric
        self.communityText = pygwidgets.DisplayText(window, (50, 0), '', fontSize=24, textColor=PURPLE)
        self.totalEVsText = pygwidgets.DisplayText(window, (50, 20), '', fontSize=24)
        self.totalCostText = pygwidgets.DisplayText(window, (50, 160), '', fontSize=24)
        self.totalCostText2 = pygwidgets.DisplayText(window, (50, 180), '', fontSize=24)

        self.totalEVsChargedDaily = pygwidgets.DisplayText(window, (50, 40), '', fontSize=24)
        self.totalCostChargedWeekly = pygwidgets.DisplayText(window, (50, 60), '', fontSize=24)

        self.vehicleNotCharged = pygwidgets.DisplayText(window, (50, 100), '', fontSize=24)
        self.vehicleNotChargedWeekly = pygwidgets.DisplayText(window, (50, 120), '', fontSize=24)

        self.additionalCharger2 = pygwidgets.DisplayText(window, (50, 220), '', fontSize=24, textColor=PURPLE)
        self.additionalCharger3 = pygwidgets.DisplayText(window, (50, 240), '', fontSize=24, textColor=PURPLE)
        
        self.infoDic = {}

        self.finishButton = pygwidgets.TextButton(window, (350, 260), 'Finish')
        self.mainMenuButton = pygwidgets.TextButton(window, (350, 0), 'Main Menu')

    def getSceneKey(self):
      return SCENE_D

    def receive(self, receiveID, info):
          self.infoDic.update(info)
  
    def update(self):
        # Calculate results based on data passed to this scene
        totalEVs = self.infoDic['Level 2 Evs'] + self.infoDic['Level 3 Evs']
        totallevel2kw = self.infoDic['Level 2 Evs'] * 40
        totallevel3kw = self.infoDic['Level 3 Evs'] * 80
        totalCostDay = (totallevel2kw + totallevel3kw) * 0.11  
        totalCostWeek = totalCostDay * 7

        level2Cap = self.infoDic['Level 2 Capacity'] / 40
        level3Cap = self.infoDic['Level 3 Capacity'] / 80
      
        # Update DisplayText objects with calculated results        
        self.totalEVsText.setValue(f'Total EVs in community: {totalEVs}')
        self.totalEVsChargedDaily.setValue(f'Total EVs charged Daily: {(level2Cap + level3Cap):.0f}')
        self.totalCostChargedWeekly.setValue(f'Total EVs charged Weekly: {((level2Cap + level3Cap) * 7):.0f}')
        self.vehicleNotCharged.setValue(f'Total EVs not charged daily: {(totalEVs - (level2Cap + level3Cap)):.0f}')
        self.vehicleNotChargedWeekly.setValue(f'Total EVs not charged weekly: {((totalEVs - (level2Cap + level3Cap)) * 7):.0f}')
        self.totalCostText.setValue(f'Total Cost Daily: ${totalCostDay:.2f}')
        self.totalCostText2.setValue(f'Total Cost Weekly: ${totalCostWeek:.2f}')
        self.communityText.setValue(f'Community: {self.infoDic["Community"]}')

        if self.infoDic['Level 2 Evs'] - level2Cap > 0:
          self.additionalCharger2.setValue(f"{(self.infoDic['Level 2 Evs'] - level2Cap) / level2Cap:.0f} Additional Level 2 Chargers Needed.")
        if self.infoDic['Level 3 Evs'] - level3Cap > 0:
          self.additionalCharger3.setValue(f"{(self.infoDic['Level 3 Evs'] - level3Cap) / level3Cap:.0f} Additional Level 3 Chargers Needed.")
  
    def handleInputs(self, eventsList, keyPressedList):
      for event in eventsList:
        if self.mainMenuButton.handleEvent(event):
          self.goToScene(SCENE_A)
        if self.finishButton.handleEvent(event):
            pygame.quit()
            sys.exit() 
  
    def draw(self):
        self.window.fill(WHITE)
        self.finishButton.draw()
        self.totalEVsText.draw()
        self.totalEVsChargedDaily.draw()
        self.totalCostChargedWeekly.draw()
        self.vehicleNotCharged.draw()
        self.totalCostText.draw()
        self.totalCostText2.draw()
        self.communityText.draw()
        self.vehicleNotChargedWeekly.draw()
        self.additionalCharger2.draw()
        self.additionalCharger3.draw()
        self.mainMenuButton.draw()

