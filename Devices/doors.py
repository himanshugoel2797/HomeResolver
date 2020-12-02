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
