from Apps.app import App


class HVACLocationControl(App):
    def __init__(self):
        App.__init__(self, "HVAC Location Control")

    def update(self, sys):
        # Compute distance vs target temperature time to determine target heating/cooling rate
        hvac_props_h = [sys.devices["HVAC"].get_resource_usage(
            "heating", {"rate": x + 1}) for x in range(4)]
        hvac_props_c = [sys.devices["HVAC"].get_resource_usage(
            "cooling", {"rate": x + 1}) for x in range(4)]

        actions = []
        weights = []
        alt_actions = []

        # assume walking speed
        room = sys.sensors["User Locator"].get_value()
        cur_temp = sys.sensors["Thermometer"].get_value()
        target_temp = sys.target_temperature_present

        # Turn A/C off if the resident is not home.
        if room == "Out of the House":
            App.app_print("[HVAC Location Control] [HVAC] Off requested")
            return [{"device": "HVAC", "target": "off"}], [[0, 0, 0]], [], [], [], []

        if cur_temp > target_temp:
            # Cooling
            hvac_tot = [-1 * (cur_temp - target_temp) /
                        hvac_props_c[x]["temperature_delta"] for x in range(4)]

            App.app_print("[HVAC Location Control] [HVAC] Cooling requested")
            # Adjust penalties based on time difference till target temperature
            for i in range(4):
                actions.append(
                    {"device": "HVAC", "target": "cooling_%d" % (i + 1)})
                weights.append([hvac_props_c[i]["power"], 5 -
                                abs(hvac_tot[i] / 30 * 3), 0])
                alt_actions.append(i)
            return actions, weights, [], [], [], [alt_actions]

        elif cur_temp < target_temp:
            # Heating
            hvac_tot = [(target_temp - cur_temp) / hvac_props_h[x]
                        ["temperature_delta"] for x in range(4)]

            App.app_print("[HVAC Location Control] [HVAC] Heating requested")
            # Adjust penalties based on time difference till target temperature
            for i in range(4):
                actions.append(
                    {"device": "HVAC", "target": "heating_%d" % (i + 1)})
                weights.append([hvac_props_h[i]["power"], 5 -
                                abs(hvac_tot[i] / 30 * 3), 0])
                alt_actions.append(i)
            return actions, weights, [], [], [], [alt_actions]

        return [], [], [], [], [], []
