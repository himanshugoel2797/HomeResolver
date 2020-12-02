from Devices.device import Device


class BatteryBackup(Device):
    def __init__(self):
        states = ["charging, supplying, idle"]
        state_changes = {
            "idle:charging": "Charging requested",
            "supplying:charging": "Charging requested",
            "idle:supplying": "Supplying requested",
            "charging:supplying": "Supplying requested",
            "charging:idle": "Idle requested",
            "supplying:idle": "Idle requested"
        }
        variables = {
            "stored": 0,
            "consumption": 0,
        }
        Device.__init__(self, "Battery Backup", states, state_changes, variables, "idle")

    def get_resource_usage(state_trans, variables):
        return {
            "capacity": 20000 * 60 * 60,  # 20kWh
            "charging_rate": 1000,  # 1kW
        }

    def update(self, sys, env):
        cur_vars = self.get_resource_usage(self.current_state, self.variables)

        if self.current_state == "charging":
            env.update_power(cur_vars["charging_rate"])  # Consume power
            self.variables["stored"] += cur_vars["charging_rate"]
            if self.variables["stored"] >= cur_vars["capacity"]:  # Stop charging further
                self.variables["stored"] = cur_vars["capacity"]
                self.current_state = "idle"
        elif self.current_state == "supplying":  # Supply as much power as available
            if self.variables["stored"] >= self.variables["consumption"]:
                self.variables["stored"] -= self.variables["consumption"]
                env.update_power(-self.variables["consumption"])
            else:
                env.update_power(-self.variables["stored"])
                self.variables["stored"] = 0
                self.current_state = "idle"
