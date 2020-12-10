from Apps.app import App


class FakeActivity(App):
    time_on = 0
    transition_counter_in = 0
    transition_counter_out = 0
    cur_state = "start_pending"

    def __init__(self, start_time, wake_duration):
        App.__init__(self, "Fake Activity")
        self.start_time = start_time
        self.wake_duration = wake_duration

    def update(self, sys):
        if not sys.sensors["Presence Sensor"].value:
            if self.cur_state == "start_pending" and self.start_time >= sys.rounded_time:
                self.cur_state = "started"
                self.counter = 0
            elif self.cur_state == "started" and self.counter < self.wake_duration:
                #Submit lights on request
                self.counter += 1
                return [{"device": "Indoor Lights", "target": "on"}], [[sys.devices["Indoor Lights"].get_resource_usage("on", None)["power"], 0, 10]], [], [], [], []
            elif self.cur_state == "started" and self.counter >= self.wake_duration:
                self.cur_state = "start_pending"
                return [{"device": "Indoor Lights", "target": "off"}], [[0, 0, 10]], [], [], [], []
        else:
            self.cur_state = "start_pending"
        return [], [], [], [], [], []
