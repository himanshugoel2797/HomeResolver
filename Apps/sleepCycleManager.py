from Apps.app import App


class SleepCycleManager(App):
    current_state = "sleep_pending"
    transition_counter = 0  # 5 minutes

    def __init__(self, sleep_time, wake_time):
        App.__init__(self, "Sleep Cycle Manager")
        self.sleep_time = sleep_time
        self.wake_time = wake_time
        self.transition_time = 5

    def update(self, sys):
        if self.current_state == "wake_pending" and sys.rounded_time >= self.wake_time:
            # Transition to wake mode
            self.current_state = "wake_processing"
            self.transition_counter = 0

        elif self.current_state == "wake_processing":
            # Set system to sleep pending
            self.transition_counter += 1
            # Slowly raise blinds
            if self.transition_counter == 50:
                self.current_state = "sleep_pending"

            App.app_print("[Sleep Cycle Manager] [Blinds] Blinds raised requested")

            actions = []
            weights = []

            all_devs = sys.all_devs_of_type("Blinds_")
            for dev in all_devs:
                actions.append(
                    {"device": dev, "target": "raised_%d" % (self.transition_counter / 10)})
                weights.append([0, self.transition_counter / 10, 0])

            all_devs = sys.all_devs_of_type("Lights_")
            for dev in all_devs:
                actions.append({"device": dev, "target": "on"})
                weights.append([sys.devices[dev].get_resource_usage("on", None)[
                               "power"], self.transition_counter / 10, 0])

            all_devs = sys.all_devs_of_type("Windows_")
            for dev in all_devs:
                actions.append({"device": dev, "target": "open"})
                weights.append([0, self.transition_counter / 10, 0])

            return actions, weights, [], [], [], []

        elif self.current_state == "sleep_pending" and sys.rounded_time >= self.sleep_time:
            # Transition to sleep mode
            self.current_state = "sleep_processing"
            self.transition_counter = 0

        elif self.current_state == "sleep_processing":
            # Set system to wake pending
            self.transition_counter += 1
            # Slowly lower blinds
            if self.transition_counter == 50:
                self.current_state = "sleep_pending"

            App.app_print("[Sleep Cycle Manager] [Blinds] Blinds lowered requested")
            actions = [{"device": "Blinds", "target": "lowered_%d" % (self.transition_counter / 10)},
                       {"device": "Indoor Lights", "target": "off"},
                       {"device": "Windows", "target": "closed"}]
            weights = [[0, self.transition_counter / 10, 2],
                       [0, self.transition_counter / 10, 2],
                       [0, self.transition_counter / 10, 2]]

            actions = []
            weights = []

            all_devs = sys.all_devs_of_type("Blinds_")
            for dev in all_devs:
                actions.append(
                    {"device": dev, "target": "lowered_%d" % (self.transition_counter / 10)})
                weights.append([0, self.transition_counter / 10, 0])
                
            all_devs = sys.all_devs_of_type("Lights_")
            for dev in all_devs:
                actions.append({"device": dev, "target": "off"})
                weights.append([0, self.transition_counter / 10, 0])
                
            all_devs = sys.all_devs_of_type("Windows_")
            for dev in all_devs:
                actions.append({"device": dev, "target": "closed"})
                weights.append([0, self.transition_counter / 10, 0])

            return actions, weights, [], [], [], []

        return [], [], [], [], [], []
