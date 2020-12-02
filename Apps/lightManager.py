from Apps.app import App


class LightManager(App):
    current_state = "on_pending"

    def __init__(self, sunset_time, sunrise_time):
        App.__init__(self, "Light Manager")
        self.sunset_time = sunset_time
        self.sunrise_time = sunrise_time
        self.time_on = self.sunrise_time - self.sunset_time
        if self.time_on < 0:
            self.time_on += 24 * 60 * 60

    def update(self, sys):
        if self.current_state == "on_pending" and sys.rounded_time >= self.sunset_time:
            # Request lights on
            self.current_state = "off_pending"
            return [{"device": "Indoor Lights", "target": "on", "timeout": self.time_on, "timeout_target": "off"}], [[sys.devices["Indoor Lights"].GetResourceUsage("on", None)["power"], 8, 10]], [], [], []
        elif self.current_state == "off_pending" and sys.rounded_time >= self.sunrise_time:
            # Request lights off
            self.current_state = "on_pending"
            return [{"device": "Indoor Lights", "target": "off"}], [[0, 8, 0]], [], [], []
        return [], [], [], [], []
