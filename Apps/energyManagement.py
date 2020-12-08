from Apps.app import App


class EnergyManagement(App):
    # Track total energy bill
    # Apply strict power constraint based on that
    def __init__(self, target_elect_bill):
        self.target_elect_bill = target_elect_bill
        self.cur_bill = 0
        App.__init__(self, "Energy Management")

    def update(self, sys):
        elect_rate = sys.sensors["Power Rate"].get_value()
        elect_cons = sys.sensors["Power Meter"].get_value()

        inst_cost = elect_cons * elect_rate
        self.cur_bill += inst_cost
        avail_cost = self.target_elect_bill - self.cur_bill
        avail_inst_pwr = avail_cost / elect_rate
        sys.set_max_power_limit(avail_inst_pwr)

        return [], [], [], [], [], []
