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
        App.app_print("[Fake Activity] [Indoor Lights] Lights on requested")

        act_list = []
        weight_list = []

        all_devs = sys.all_devs_of_type("Lights_")
        for dev in all_devs:
            act_list.append({"device": dev, "target": "on"})
            weight_list.append([sys.devices[dev].get_resource_usage("on", None)["power"], 0, 5])

        return act_list, weight_list, [], [], [], []

    @staticmethod
    def off(sys):
        App.app_print("[Fake Activity] [Indoor Lights] Lights off requested")

        act_list = []
        weight_list = []

        all_devs = sys.all_devs_of_type("Lights_")
        for dev in all_devs:
            act_list.append({"device": dev, "target": "off"})
            weight_list.append(
                [0, 0, 3])

        return act_list, weight_list, [], [], [], []

    def update(self, sys):
        if not sys.sensors["Presence Sensor"].value and self.sunset_time >= sys.rounded_time >= self.sunrise_time:
            self.counter += 1

            if self.cur_state == "start_pending":
                if self.counter >= self.time_off:
                    self.cur_state = "started"
                    self.counter = 0
                    self.on(sys)
                else:
                    return self.off(sys)
            else:
                if self.counter >= self.time_on:
                    self.cur_state = "state_pending"
                    self.counter = 0
                    return self.off(sys)
                else:
                    return self.on(sys)
        elif self.cur_state == "started":
            return self.off()
        return [], [], [], [], [], []
