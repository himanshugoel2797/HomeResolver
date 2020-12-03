from Apps.app import App


class IntruderPrevention(App):
    current_state = "on_pending"

    def __init__(self, on_time, off_time):
        App.__init__(self, "Intruder Prevention")
        self.on_time = on_time
        self.off_time = off_time

    def update(self, sys):
        if self.current_state == "on_pending" and sys.rounded_time >= self.on_time:
            # Request lights on or motion sensing
            self.current_state = "off_pending"
            self.transition_counter = 0
            # requested_actions, weight_sets, mandatory_actions, contradicting_action_pairs, dependent_action_pairs, alternative_actions
            return [{"device": "Outdoor Lights", "target": "off"}], [[0, 0, 9]], [], [], [], []
        elif self.current_state == "off_pending" and sys.rounded_time >= self.off_time:
            # Request lights off
            self.current_state = "on_pending"
            self.transition_counter = 0
            # requested_actions, weight_sets, mandatory_actions, contradicting_action_pairs, dependent_action_pairs, alternative_actions
            return [{"device": "Outdoor Lights", "target": "on"}], [[0, 0, 9]], [], [], [], []
        return [], [], [], [], [], []
