from Apps.app import App


class LightManager(App):
    def __init__(self, sunrise_time, sunset_time):
        App.__init__(self, "Light Manager")
        self.sunrise_time = sunrise_time
        self.sunset_time = sunset_time

    def update(self, sys):
        if self.sunrise_time <= sys.rounded_time <= self.sunset_time:
            print("[Light Manager] [Indoor Lights] Lights on requested")
            return [{"device": "Indoor Lights", "target": "on"}], \
                   [[sys.devices["Indoor Lights"].get_resource_usage("on", None)["power"], 8, 10]], [], [], [], []
        else:
            print("[Light Manager] [Indoor Lights] Lights off requested")
            return [{"device": "Indoor Lights", "target": "off"}], [[0, 8, 0]], [], [], [], []
