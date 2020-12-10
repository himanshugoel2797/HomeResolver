from Apps.app import App


class HVACPowerControl(App):
    def __init__(self):
        App.__init__(self, "HVAC Power Control")

    def update(self, sys):
        cur_temp = sys.sensors["Thermometer"].get_value()
        present = sys.sensors["Presence Sensor"].get_value()

        actions = []
        weights = []
        alternative_actions = []

        if present:
            target = sys.target_temperature_present
            if cur_temp < target: # Heat
                for i in range(4):
                    actions.append({"device": "HVAC", "target": "heating_%d" % (i + 1)})
                    resources = sys.devices["HVAC"].get_resource_usage("heating", {"rate" : i + 1})
                    weights.append([resources["power"], target - cur_temp, 0])
                    alternative_actions.append(i)
            elif cur_temp > target: # Cool
                for i in range(4):
                    actions.append({"device": "HVAC", "target": "cooling_%d" % (i + 1)})
                    resources = sys.devices["HVAC"].get_resource_usage("cooling", {"rate" : i + 1})
                    weights.append([resources["power"], cur_temp - target, 0])
                    alternative_actions.append(i)
            else:
                return [], [], [], [], [], []
            return actions, weights, [], [], [], [alternative_actions]
        else:
            target = sys.target_temperature_absent
            if cur_temp < target: # Heat
                for i in range(4):
                    actions.append({"device": "HVAC", "target": "heating_%d" % (i + 1)})
                    resources = sys.devices["HVAC"].get_resource_usage("heating", {"rate" : i + 1})
                    weights.append([resources["power"], target - cur_temp, 0])
                    alternative_actions.append(i)
            elif cur_temp > target: # Cool
                for i in range(4):
                    actions.append({"device": "HVAC", "target": "cooling_%d" % (i + 1)})
                    resources = sys.devices["HVAC"].get_resource_usage("cooling", {"rate" : i + 1})
                    weights.append([resources["power"], cur_temp - target, 0])
                    alternative_actions.append(i)
            else:
                return [], [], [], [], [], []
            return actions, weights, [], [], [], [alternative_actions]
