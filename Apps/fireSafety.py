from Apps.app import App


class FireSafety(App):
    def __init__(self):
        App.__init__(self, "Sleep Cycle Manager")

    def update(self, sys):
        if sys.sensors["Smoke Detector"].value:
            # requested_actions, weight_sets, mandatory_actions, alternative_action_pairs, exclusive_action_pairs
            return [{"device": "Doors", "target": "opened", "timeout": -1}], [[0, 1, 10]], [0], [], []
        return [], [], [], [], []
