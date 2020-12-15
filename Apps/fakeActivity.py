from Apps.app import App


class FakeActivity(App):
    time_on = 0
    counter = 0
    cur_state = "start_pending"

    def __init__(self, sunrise_time, sunset_time, time_on, time_off):
        App.__init__(self, "Fake Activity")
        self.sunrise_time = sunrise_time
        self.sunset_time = sunset_time
        self.time_on = time_on
        self.time_off = time_off
        self.counter = time_off

    @staticmethod
    def on(sys):
        print("[Fake Activity] [Indoor Lights] Lights on requested")
        return [{"device": "Indoor Lights", "target": "on"}], \
               [[sys.devices["Indoor Lights"].get_resource_usage("on", None)["power"], 0,
                 10]], [], [], [], []

    @staticmethod
    def off():
        print("[Fake Activity] [Indoor Lights] Lights off requested")
        return [{"device": "Indoor Lights", "target": "off"}], [[0, 0, 10]], [], [], [], []

    def update(self, sys):
        if not sys.sensors["Presence Sensor"].value and self.sunset_time >= sys.rounded_time >= self.sunrise_time:
            self.counter += 1

            if self.cur_state == "start_pending":
                if self.counter >= self.time_off:
                    self.cur_state = "started"
                    self.counter = 0
                    self.on(sys)
                else:
                    return self.off()
            else:
                if self.counter >= self.time_on:
                    self.cur_state = "state_pending"
                    self.counter = 0
                    return self.off()
                else:
                    return self.on(sys)
        elif self.cur_state == "started":
            return self.off()
        return [], [], [], [], [], []
