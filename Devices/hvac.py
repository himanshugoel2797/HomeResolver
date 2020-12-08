from Devices.device import Device


class HVAC(Device):
    temperature_curve = [0, 1 / (2 * 60), 1.3 / (2 * 60), 1.5 / (2 * 60), 2 / (2 * 60)]  # Degrees change per second
    energy_curve = [0, 50, 125, 200, 300]

    def __init__(self):
        states = ["heating", "cooling", "off"]
        state_changes = {
            "off:heating": "Heating requested",
            "cooling:heating": "Heating requested",
            "off:cooling": "Cooling requested",
            "heating:cooling": "Cooling requested",
            "heating:off": "Off requested",
            "cooling:off": "Off requested"
        }
        variables = {
            "rate": 1,
        }
        Device.__init__(self, "HVAC", states, state_changes, variables, "off")

    def get_resource_usage(self, state_trans, variables):
        if state_trans.endswith("heating"):
            return {
                "power": self.energy_curve[variables["rate"]] * 1.2,
                "temperature_delta": self.temperature_curve[variables["rate"]],
            }
        elif state_trans.endswith("cooling"):
            return {
                "power": self.energy_curve[variables["rate"]],
                "temperature_delta": -self.temperature_curve[variables["rate"]],
            }
        else:
            return {
                "power": 0,
                "temperature_delta": 0,
            }

    def update(self, sys, env):
        cur_vars = self.get_resource_usage(self.current_state, self.variables)
        env.update_power(cur_vars["power"])  # Consume power
        env.update_temperature(cur_vars["temperature_delta"])  # Update current temperature
