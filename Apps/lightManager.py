from Apps.app import App


class LightManager(App):
    def __init__(self, sunrise_time, sunset_time):
        App.__init__(self, "Light Manager")
        self.sunrise_time = sunrise_time
        self.sunset_time = sunset_time

    def update(self, sys):
        if self.sunrise_time <= sys.rounded_time <= self.sunset_time:
            App.app_print(
                "[Light Manager] [Indoor Lights] Lights on requested")
            act_list = []
            weight_list = []

            all_devs = sys.all_devs_of_type("Lights_")
            for dev in all_devs:
                act_list.append({"device": dev, "target": "on"})
                weight_list.append([sys.devices[dev].get_resource_usage("on", None)["power"], 8, 10])

            return act_list, weight_list, [], [], [], []
        else:
            App.app_print(
                "[Light Manager] [Indoor Lights] Lights off requested")

            act_list = []
            weight_list = []

            all_devs = sys.all_devs_of_type("Lights_")
            for dev in all_devs:
                act_list.append({"device": dev, "target": "off"})
                weight_list.append([0, 8, 0])

            return act_list, weight_list, [], [], [], []
