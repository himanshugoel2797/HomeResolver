from Apps.app import App


class HVACLocationControl(App):
    def __init__(self, target_temp):
        App.__init__(self, "HVAC Location Control")
        self.target_temp = target_temp

    def update(self, sys):
        # Compute distance vs target temperature time to determine target heating/cooling rate
        hvac_props_h = [sys.devices["HVAC"].get_resource_usage("heating", {"rate": x + 1}) for x in range(4)]
        hvac_props_c = [sys.devices["HVAC"].get_resource_usage("cooling", {"rate": x + 1}) for x in range(4)]

        actions = []
        weights = []
        alt_actions = []

        # assume walking speed
        time_avail = sys.sensors["User Locator"].get_value() / 1.4  # m/s
        cur_temp = sys.sensors["Thermometer"].get_value()
        if cur_temp > self.target_temp:
            # Cooling
            hvac_tot = [(cur_temp - self.target_temp) / hvac_props_c[x].temperature_delta for x in range(4)]

        elif cur_temp < self.target_temp:
            # Heating
            hvac_tot = [(cur_temp - self.target_temp) / hvac_props_h[x].temperature_delta for x in range(4)]

        return actions, weights, [], alt_actions, []
