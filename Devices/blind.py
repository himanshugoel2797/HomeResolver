from Devices.device import Device


class Blind(Device):
    def __init__(self):
        states = ["raised", "lowered"]
        state_changes = {
            "raised:lowered": "Lower blinds requested",
            "lowered:raised": "Raise blinds requested",
        }
        variables = {
            "shutter_amount": 0
        }
        Device.__init__(self, "Blinds", states, state_changes, variables, "lowered")

    def get_resource_usage(self, state_trans, variables):
        if state_trans.endswith("lowered"):
            return {
                "brightness_mult": (4 - variables["shutter_amount"]) * 0.25,
            }
        elif state_trans.endswith("raised"):
            return {
                "brightness_mult": 1,
            }
        else:
            return None

    def update(self, sys, env):
        cur_vars = self.get_resource_usage(self.current_state, self.variables)
        env.set_ambient_light_mult(cur_vars["brightness_mult"])
        
    def transition_state(self, target_state_name):
        parts = target_state_name.split('_')
        lv = int(parts[1])
        target_state_name = parts[0]
        if self.current_state != target_state_name and target_state_name in self.states:
            state_change = self.current_state + ":" + target_state_name
            for k, v in self.state_changes.items():
                if k == state_change:
                    print ("[%s] %s, lv: %d" % (self.name, v, lv)) # Use value.
            self.current_state = target_state_name
