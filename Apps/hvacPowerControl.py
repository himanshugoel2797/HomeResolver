from Apps.app import App


class HVACPowerControl(App):
    def __init__(self):
        App.__init__(self, "HVAC Power Control")

    def update(self, sys):
        thermometers = sys.all_sensors_of_type("Thermometer")
        cur_temp = []
        for i in range(len(thermometers)):
            cur_temp.append(sys.sensors[thermometers[i]].get_value())
        present = sys.sensors["Presence Sensor"].get_value()

        actions = []
        weights = []
        alt_actions = []

        hvacs = sys.all_devs_of_type("HVAC")
        count = 0

        if present:
            target = sys.target_temperature_present
        else:
            target = sys.target_temperature_absent
        for i in range(len(cur_temp)):
            if cur_temp[i] < target:  # Heat
                for j in range(4):
                    room_name = thermometers[i].room_name
                    actions.append({"device": "HVAC_%s" % (room_name), "target": "heating_%d" % (j + 1)})
                    resources = sys.devices["HVAC_%s" % (room_name)].get_resource_usage("heating", {"rate": j + 1})
                    weights.append([resources["power"], (target - cur_temp[i]) * (j + 1) * 0.2, 0])
                    alt_actions.append(count)
                    count += 1
            elif cur_temp[i] > target:  # Cool
                for j in range(4):
                    room_name = thermometers[i].room_name
                    actions.append({"device": "HVAC_%s" % (room_name), "target": "cooling_%d" % (j + 1)})
                    resources = sys.devices["HVAC_%s" % (room_name)].get_resource_usage("cooling", {"rate": j + 1})
                    weights.append([resources["power"], (cur_temp[i] - target) * (j + 1) * 0.2, 0])
                    alt_actions.append(count)
                    count += 1
        if len(alt_actions) > 0:
            return actions, weights, [], [], [], [alt_actions]
        return actions, weights, [], [], [], []
