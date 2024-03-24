from abc import ABC, abstractmethod

class ChargingStation(ABC):
    def __init__(self, capacity, level):
        self.capacity = capacity
        self.level = level

    @abstractmethod
    def calculate_daily_cost(self):
        pass

    @abstractmethod
    def charge_ev(self, ev):
        pass

    @abstractmethod
    def number_charger(self):
        pass

    @abstractmethod
    def add_charger(self, level, number):
        pass

    @abstractmethod
    def get_total_capacity(self):
        pass