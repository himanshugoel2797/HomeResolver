from Apps.app import App


class FireSafety(App):
    def __init__(self):
        App.__init__(self, "Fire Safety")

    def update(self, sys):
        sens_vals = sys.all_sensors_of_type("Smoke Detector")
        for s in sens_vals:
            if sys.sensors[s].value:
                # requested_actions, weight_sets, mandatory_actions,
                # contradicting_action_pairs, dependent_action_pairs, alternative_actions
                App.app_print("[Fire Safety] [Doors] Doors opened requested")
                acts, weights, mandatory, _ = sys.all_action("Door_", "opened", [0, 0, 10], 0)
                return acts, weights, mandatory, [], [], []
        return [], [], [], [], [], []
