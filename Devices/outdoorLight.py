from Devices.device import Device


class OutdoorLight(Device):
    def __init__(self, name):
        states = ["on", "off"]
        state_changes = {
            "off:on": "Lights on requested",
            "on:off": "Lights off requested",
        }
        variables = {
            "level": 0
        }
        Device.__init__(self, name, states, state_changes, variables, "off")

    def get_resource_usage(self, state_trans, variables):
        if state_trans.endswith("on"):
            return {
                "brightness": variables["level"] * 0.25,
                "power": variables["level"] * 2.5,
            }
        elif state_trans.endswith("off"):
            return {
                "brightness": 0,
                "power": 0,
            }
        else:
            return None

    def update(self, sys, env):
        cur_vars = self.get_resource_usage(self.current_state, self.variables)
        env.update_power(cur_vars["power"])  # Consume power
        env.add_light(cur_vars["brightness"])  # Update light amount
