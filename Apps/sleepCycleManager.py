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

            print("[Sleep Cycle Manager] [Blinds] Blinds raised requested")
            return [{"device": "Blinds", "target": "raised_%d" % (self.transition_counter / 10)}], [[0, self.transition_counter / 10, 2]], [], [], [], []
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

            print("[Sleep Cycle Manager] [Blinds] Blinds lowered requested")
            return [{"device": "Blinds", "target": "lowered_%d" % (self.transition_counter / 10)}], [[0, self.transition_counter / 10, 5]], [], [], [], []
        return [], [], [], [], [], []