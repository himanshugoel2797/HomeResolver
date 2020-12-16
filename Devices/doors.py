from Devices.device import Device


class Doors(Device):
    def __init__(self):
        states = ["opened", "closed"]
        state_changes = {
            "opened:closed": "Closed doors requested",
            "closed:opened": "Opened doors requested"
        }
        Device.__init__(self, "Doors", states, state_changes, {}, "closed")

    def get_resource_usage(self, state_trans, variables):
        return {}

    def update(self, sys, env):
        pass

    def transition_state(self, target_state_name):
        if target_state_name in self.states:
            state_change = self.current_state + ":" + target_state_name
            for k, v in self.state_changes.items():
                if k == state_change:
                    Device.dev_print("[%s] %s" % (self.name, v))  # Use value.
            self.current_state = target_state_name
