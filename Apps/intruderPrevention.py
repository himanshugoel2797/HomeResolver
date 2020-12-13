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
            # requested_actions, weight_sets, mandatory_actions,
            # contradicting_action_pairs, dependent_action_pairs, alternative_actions

            req_actions = []
            weights = []
            alt_actions = []

            print("[Intruder Prevention] [Outdoor Lights] Lights on requested")
            print("[Intruder Prevention] [Outdoor Lights] Motion sensor requested")
            for i in range(5):  # 5 brightness levels
                req_actions.append({"device": "Outdoor Lights", "target": "on_%d" % (i)})
                weights.append([sys.devices["Outdoor Lights"].get_resource_usage("on", {"level":i})["power"], 0, 4 + i])
                
                req_actions.append({"device": "Outdoor Lights", "target": "motionsensor_%d" % (i)})
                weights.append([sys.devices["Outdoor Lights"].get_resource_usage("motionsensor", {"level":i})["power"], 0, 1 + i])
                
                alt_actions.append(i * 2 + 0)
                alt_actions.append(i * 2 + 1)

            return req_actions, weights, [], [], [], [alt_actions]
        elif self.current_state == "off_pending" and sys.rounded_time >= self.off_time:
            # Request lights off
            self.current_state = "on_pending"
            print("[Intruder Prevention] [Outdoor Lights] Lights off requested")
            # requested_actions, weight_sets, mandatory_actions,
            # contradicting_action_pairs, dependent_action_pairs, alternative_actions
            return [{"device": "Outdoor Lights", "target": "off"}], [[0, 0, 9]], [], [], [], []
        return [], [], [], [], [], []
