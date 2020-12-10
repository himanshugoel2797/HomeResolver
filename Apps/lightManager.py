from Apps.app import App


class LightManager(App):
    current_state = "on_pending"

    def __init__(self, sunset_time, sunrise_time):
        App.__init__(self, "Light Manager")
        self.sunset_time = sunset_time
        self.sunrise_time = sunrise_time

    def update(self, sys):
        if self.current_state == "on_pending" and sys.rounded_time >= self.sunset_time:
            # Request lights on
            self.current_state = "off_pending"
            print("[Light Manager] [Indoor Lights] Lights on requested")
            return [{"device": "Indoor Lights", "target": "on"}], [[sys.devices["Indoor Lights"].get_resource_usage("on", None)["power"], 8, 10]], [], [], [], []
        elif self.current_state == "off_pending" and sys.rounded_time >= self.sunrise_time:
            # Request lights off
            self.current_state = "on_pending"
            print("[Light Manager] [Indoor Lights] Lights on requested")
            return [{"device": "Indoor Lights", "target": "off"}], [[0, 8, 0]], [], [], [], []
        return [], [], [], [], [], []
