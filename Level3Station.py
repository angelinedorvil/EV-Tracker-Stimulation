from ChargingStation import ChargingStation

class Level3Station(ChargingStation):
    COST_PER_KWH = 0.11 # Cost of electricity per kWh
    CAPACITY_KW = 1500 # Capacity of the charging station in kW per day
    QUANTITY_OF_CHARGERS = 7 # Number of chargers in the station
  
    def __init__(self):
        super().__init__(self.CAPACITY_KW, 3)
  
    def calculate_daily_cost(self, kwh_used):
        """Calculate and return the daily cost of electricity used."""
        return kwh_used * self.COST_PER_KWH
  
    def charge_ev(self, ev):
        if ev.capacity <= self.capacity:
          print(f"Charging {ev} at Level 2 Station")
          # Implement the charging logic based on EV's capacity and update the station's capacity accordingly.
        else:
          print("EV capacity exceeds this station's limit.")
  
    def number_charger(self):
        return self.QUANTITY_OF_CHARGERS
  
    def add_charger(self, level, number):
        if level == 3:
            self.QUANTITY_OF_CHARGERS += number
            self.CAPACITY_KW += (number * 1500)

    def get_total_capacity(self):
      return self.CAPACITY_KW