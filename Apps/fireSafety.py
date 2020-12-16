from Apps.app import App


class FireSafety(App):
    def __init__(self):
        App.__init__(self, "Fire Safety")

    def update(self, sys):
        if sys.sensors["Smoke Detector"].value:
            # requested_actions, weight_sets, mandatory_actions,
            # contradicting_action_pairs, dependent_action_pairs, alternative_actions
            App.app_print("[Fire Safety] [Doors] Doors opened requested")
            return [{"device": "Doors", "target": "opened"}], [[0, 0, 10]], [0], [], [], []
        return [], [], [], [], [], []
