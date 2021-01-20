from Apps.app import App


class HVACLocationControl(App):
    def __init__(self):
        App.__init__(self, "HVAC Location Control")

    def update(self, sys):
        room_name = sys.sensors["User Locator"].get_value()
        # Turn A/C off if the resident is not home.
        if room_name.startswith("outside_"):
            App.app_print("[HVAC Location Control] [HVAC] Off requested")

            act_list, weight_list, _, _ = sys.all_action("HVAC", "off", [0, 0, 0], 0)
            return act_list, weight_list, [], [], [], []

        # Compute distance vs target temperature time to determine target heating/cooling rate
        hvac_props_h = \
            [sys.devices["HVAC_%s" % (room_name)].get_resource_usage("heating", {"rate": x + 1}) for x in range(4)]
        hvac_props_c = \
            [sys.devices["HVAC_%s" % (room_name)].get_resource_usage("cooling", {"rate": x + 1}) for x in range(4)]

        actions = []
        weights = []
        alt_actions = []

        target_temp = sys.target_temperature_present

        cur_temp = sys.sensors["Thermometer_%s" % room_name].get_value()

        if cur_temp > target_temp:
            # Cooling
            hvac_tot = [-1 * (cur_temp - target_temp) / hvac_props_c[x]["temperature_delta"] for x in range(4)]

            App.app_print("[HVAC Location Control] [HVAC] Cooling requested")
            # Adjust penalties based on time difference till target temperature
            for i in range(4):
                actions.append({"device": "HVAC_%s" % (room_name), "target": "cooling_%d" % (i + 1)})
                weights.append([hvac_props_c[i]["power"], 5 - abs(hvac_tot[i] / 30 * 3), 0])
                alt_actions.append(i)
            return actions, weights, [], [], [], [alt_actions]

        elif cur_temp < target_temp:
            # Heating
            hvac_tot = [(target_temp - cur_temp) / hvac_props_h[x]
                        ["temperature_delta"] for x in range(4)]

            App.app_print("[HVAC Location Control] [HVAC] Heating requested")
            # Adjust penalties based on time difference till target temperature
            for i in range(4):
                actions.append({"device": "HVAC_%s" % (room_name), "target": "heating_%d" % (i + 1)})
                weights.append([hvac_props_h[i]["power"], 5 - abs(hvac_tot[i] / 30 * 3), 0])
                alt_actions.append(i)
            return actions, weights, [], [], [], [alt_actions]

        return [], [], [], [], [], []
