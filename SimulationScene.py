import pygwidgets
import pygame
from pyghelpers import Scene
from constants import WHITE, SCENE_C, SCENE_D, PURPLE, TEAL, BLUE, YELLOW



class SimulationScene(Scene):
    REMOVE = False
    ADD = False
    START = False
    DAY = False
    def __init__(self, window):
      self.window = window
      self.infoDic = {}
      self.resultsButton = pygwidgets.TextButton(window, (320, 0), 'Go Back to Results')
      self.addText = 0
      self.removeText = 0
      self.level3Charge = 7
      self.leve3Evs = 0

      # Initialize DisplayText objects for each result metric
      self.communityText = pygwidgets.DisplayText(window, (30, 0), '', fontSize=24, textColor=PURPLE)
      self.level3Station = pygwidgets.DisplayText(window, (30, 40), '', fontSize=24)
      self.level3StationStimulation = pygwidgets.DisplayText(window, (30, 60), '', fontSize=24)
      self.level3StationStimulation2 = pygwidgets.DisplayText(window, (30, 80), '', fontSize=24, textColor=PURPLE)
      self.level3StationStimulation3 = pygwidgets.DisplayText(window, (30, 100), '', fontSize=24)
      self.surpluxSim = pygwidgets.DisplayText(window, (0, 140), '', fontSize=24, textColor=BLUE)

      self.newCharger = pygwidgets.DisplayText(window, (0, 180), 'Add new level 3 charger', fontSize=24, justified='left')
      self.inputEvCharger = pygwidgets.InputText(window, (200, 180), width=120, backgroundColor=TEAL)
      self.addButton = pygwidgets.TextButton(window, (350, 160), 'Add', fontSize=18)

      self.removeCharger = pygwidgets.DisplayText(window, (0, 220), 'Remove new level 3 charger', fontSize=24, justified='left')
      self.removeEvCharger = pygwidgets.InputText(window, (240, 220), width=100, backgroundColor=TEAL)
      self.removeButton = pygwidgets.TextButton(window, (350, 220), 'Remove', fontSize=18)

      self.chargerNeeded = pygwidgets.DisplayText(window, (30, 20), '', fontSize=24)
      self.additionalLevel3 = 0
      self.level3Cap = 0

      self.displayTime = pygwidgets.DisplayText(self.window, (350, 0), '')
      self.startButton = pygwidgets.TextButton(window, (50, 250), 'Start hourly')
      self.oneDayButton = pygwidgets.TextButton(window, (180, 250), 'Start 24hrs')

      self.restartButton = pygwidgets.TextButton(window, (350, 80), 'Restart', textColor=YELLOW)

    def getSceneKey(self):
      return SCENE_C

    def receive(self, receiveID, info):
      self.infoDic = info
      
    def handleInputs(self, eventsList, keyPressedList):
      for event in eventsList:
        self.inputEvCharger.handleEvent(event)
        self.removeEvCharger.handleEvent(event)

        if self.addButton.handleEvent(event) and self.inputEvCharger.getValue().isdigit():
            self.ADD = True
            self.addText = self.inputEvCharger.getValue()

        if self.removeButton.handleEvent(event) and self.removeEvCharger.getValue().isdigit():
            self.REMOVE = True
            self.removeText = self.removeEvCharger.getValue()
          
        if self.resultsButton.handleEvent(event):
            self.send(SCENE_D,'info', self.infoDic)
            self.goToScene(SCENE_D)

        if self.startButton.handleEvent(event):
            self.START = True
            self.addButton.disable()
            self.removeButton.disable()
        
        if self.oneDayButton.handleEvent(event):
            self.DAY = True
            self.addButton.disable()
            self.removeButton.disable()

        if self.restartButton.handleEvent(event):
            self.addButton.enable()
            self.removeButton.enable()
            # Reset simulation data
            self.simulatedHoursPassed = 0
            self.level3Charge = 7  # Reset to initial value
            self.level3EvsCharged = 0
            self.START = False
            self.DAY = False
            self.ADD = False
            self.REMOVE = False
            self.surpluxSim.setValue('')
            self.level3StationStimulation.setValue('')
            self.level3StationStimulation2.setValue('')
            self.displayTime.setValue(f'{0}')
          
            
  
    def update(self):
        self.level3Station.setValue(f'Level 3 Installed stations: {7}')
        self.communityText.setValue(f'Community: {self.infoDic["Community"]}')
      
        if self.ADD:
            self.level3Charge += int(self.addText)
        self.ADD = False
      
        if self.REMOVE:
          if (self.level3Charge - int(self.removeText)) < 0:
              self.level3Charge = 0
          else:
              self.level3Charge -= int(self.removeText)
        self.REMOVE = False

        self.level3StationStimulation3.setValue(f'Level 3 Stations SIMULATION: {self.level3Charge}')

        # Capacities of chargers for number of cars
        self.level3Cap = self.infoDic['Level 3 Capacity'] / 80

        if self.infoDic['Level 3 Evs'] - self.level3Cap > 0:
          self.additionalLevel3 = (self.infoDic['Level 3 Evs'] - self.level3Cap) / self.level3Cap  # Additional Level 3 Chargers Needed
        self.chargerNeeded.setValue(f'Total Level 3 Stations Needed: {self.additionalLevel3 + 7:.0f}')

        if self.DAY:
          # Simulated charging logic
          # Let's say you decide to simulate charging 5 EVs per hour for simplicity
          if not hasattr(self, 'simulatedHoursPassed'):
              self.simulatedHoursPassed = 0  # Initialize if not already
  
          if self.simulatedHoursPassed < 25:  # Only update EVs charged if under 24 hours
              self.displayTime.setValue(f'Hour: {self.simulatedHoursPassed}')
              self.simulatedHoursPassed += 1
              evsCharged = self.simulatedHoursPassed * self.level3Charge
              print(self.level3Charge)
              evsUncharged = max(0, self.infoDic['Level 3 Evs'] - evsCharged)
              self.level3StationStimulation.setValue(f'Charged level 3 EVs: {evsCharged}')
              self.level3StationStimulation2.setValue(f'Uncharged level 3 EVs: {evsUncharged}')
              if evsCharged > self.infoDic['Level 3 Evs']:
                self.surpluxSim.setValue(f"Too many chargers {self.infoDic['Community']} Community only has {self.infoDic['Level 3 Evs']} EVs")

              if evsCharged < self.infoDic['Level 3 Evs']:
                self.surpluxSim.setValue(f"Too few chargers {self.infoDic['Community']} Community has {self.infoDic['Level 3 Evs']} EVs")
            
        if self.START:
            # Simulated charging logic
            # Let's say you decide to simulate charging 5 EVs per hour for simplicity
            if not hasattr(self, 'simulatedHoursPassed'):
                self.simulatedHoursPassed = 0  # Initialize if not already
    
            if self.simulatedHoursPassed < 25:  # Only update EVs charged if under 24 hours
                self.displayTime.setValue(f'Hour: {self.simulatedHoursPassed}')
                self.simulatedHoursPassed += 1
                evsCharged = self.simulatedHoursPassed * self.level3Charge
                print(self.level3Charge)
                evsUncharged = max(0, self.infoDic['Level 3 Evs'] - evsCharged)
                self.level3StationStimulation.setValue(f'Charged EVs: {evsCharged}')
                self.level3StationStimulation2.setValue(f'Uncharged EVs: {evsUncharged}')
                if evsCharged > self.infoDic['Level 3 Evs']:
                  self.surpluxSim.setValue(f"Too many chargers {self.infoDic['Community']} Community only has {self.infoDic['Level 3 Evs']} EVs")

                if evsCharged < self.infoDic['Level 3 Evs']:
                  self.surpluxSim.setValue(f"Too few chargers {self.infoDic['Community']} Community has {self.infoDic['Level 3 Evs']} EVs")
  
            self.START = False
            self.DAY = False

    def draw(self):
        self.window.fill(WHITE)    
        self.resultsButton.draw()
        self.newCharger.draw()
        self.inputEvCharger.draw()
        self.addButton.draw()
        self.communityText.draw()
        self.level3Station.draw()
        self.removeCharger.draw()
        self.removeEvCharger.draw()
        self.removeButton.draw()
        self.chargerNeeded.draw()
        self.level3StationStimulation.draw()
        self.displayTime.draw()
        pygame.display.update()
        self.level3StationStimulation2.draw()
        self.startButton.draw()
        self.oneDayButton.draw()
        self.level3StationStimulation3.draw()
        self.surpluxSim.draw()
        self.restartButton.draw()