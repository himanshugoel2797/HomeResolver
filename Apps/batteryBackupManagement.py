from Apps.app import App


class BatteryBackupManagement(App):
    # Request optional charging when close to lowest
    # Offer to supply when close to highest
    def __init__(self, charge_cutoff_rate, discharge_cutoff_rate):
        self.charge_cutoff_rate = charge_cutoff_rate
        self.discharge_cutoff_rate = discharge_cutoff_rate
        App.__init__(self, "Battery Backup Management")

    def update(self, sys):
        if sys.sensors["Power Rate"].get_value() <= self.charge_cutoff_rate:
            return [{"device": "Battery Backup", "target": "charging"}], [[sys.devices["Battery Backup"].get_resource_usage("charging", {})["charging_rate"], 2, 1]], [0], [], [], [] # charge
        elif sys.sensors["Power Rate"].get_value() >= self.discharge_cutoff_rate:
            pwr_cons = sys.sensors["Power Meter"].get_value()
            sys.devices["Battery Backup"].variables["consumption"] = pwr_cons
            return [{"device": "Battery Backup", "target": "supplying"}], [[-pwr_cons, 0, 0]], [0], [], [], [] # discharge
        return [], [], [], [], [], []
