class Device:
    name = ""
    states = []  # List of state names
    state_changes = {}  # Nested dictionary describing how a given state transition affects global resources
    variables = {}  # Dictionary of device variables and their values
    current_state = None  # Current device state name

    def __init__(self, init_name, init_states, init_state_changes, init_variables, init_current_state):
        name = init_name
        states = init_states
        state_changes = init_state_changes
        variables = init_variables
        if init_current_state in states:
            current_state = init_current_state
        elif states.length > 0:
            current_state = states[0]

    def TransitionState(self, target_state_name):
        if current_state != target_state_name and target_state_name in states:
            state_change = current_state + ":" + target_state_name
            current_state = target_state_name
            for k, v in state_changes:
                if k == state_change:
                    # Use value.
                    break

    # Set a variable's value
    def SetVariable(self, var_name, var_val):
        for k, v in variables.items():
            if k == var_name:
                v = var_val
                break

class Sensor:
    name = ""
    value = None

    def __init__(self, init_name, init_value):
        name = init_name
        value = init_value

    def GetValue(self):
        return value

class App:
    name = ""

    # Process app functionality
    def Update(self, systemObj):
        pass

class System:
    devices = []
    sensors = []
    apps = []

    action_set = []

    def __init__(self):
        pass

    # Name = string with device name
    # Obj = object representing interface to device, implements Device class
    def RegisterDevice(self, obj):
        devices.append(obj);

    # Name = string with sensor name
    # obj = object representing interface to sensor, implements Sensor class
    def RegisterSensor(self, obj):
        sensors.append(obj);

    # Name = string with app name
    # obj = object representing instance of app, implements App class
    def RegisterApp(self, obj):
        apps.append(obj);

    # Print current action set
    def ShowRunningSet(self):
        print("Current action set: " + action_set + "\n", end = ",")

    # Run ILP
    # Update action set
    def Process(self):
        for app in apps:
            requested_actions = app.Update(self)

        tmp_action_set = action_set + requested_actions

# Example simulation
sys_ = System()
# Create and register devices and sensors
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
    "cooling_heating_rate": 1,
    "energy_curve": 0
}
hvac = Device("HVAC", states, state_changes, variables, "off")
sys_.RegisterDevice(hvac)

states = ["raised", "lowered"]
state_changes = {
    "raised:lowered": "Lower blinds requested",
    "lowered:raised": "Raise blinds requested",
}
variables = {
    "shutter_amount": 0
}
blinds = Device("Blinds", states, state_changes, variables, "lowered")
sys_.RegisterDevice(blinds)

states = ["opened", "closed"]
state_changes = {
    "opened:closed": "Closed doors requested",
    "closed:opened": "Opened doors requested"
}
doors = Device("Doors", states, state_changes, {}, "closed")
sys_.RegisterDevice(doors)

states = ["on", "off"]
state_changes = {
    "off:on": "Lights on requested",
    "on:off": "Lights off requested",
}
lightsOutdoor = Device("Outdoor Lights", states, state_changes, {}, "off")
sys_.RegisterDevice(lightsOutdoor)
lightsIndoor = Device("Indoor Lights", states, state_changes, {}, "off")
sys_.RegisterDevice(lightsIndoor)

states = ["charging, supplying, idle"]
state_changes = {
    "idle:charging": "Charging requested",
    "supplying:charging": "Charging requested",
    "idle:supplying": "Supplying requested",
    "charging:supplying": "Supplying requested",
    "charging:idle": "Idle requested",
    "supplying:idle": "Idle requested"
}
batteryBackup = Device("Battery Backup", states, state_changes, {}, "Idle")
sys_.RegisterDevice(batteryBackup)

human_presence_sensor = Sensor("Human Presence Sensor", False)
sys_.RegisterSensor(human_presence_sensor)

thermometer = Sensor("Thermometer", 75.00)
sys_.RegisterSensor(thermometer)

outdoor_motion_detector = Sensor("Outdoor Motion Detector", False)
sys_.RegisterSensor(outdoor_motion_detector)

power_meter = Sensor("Power Meter", 0.00)
sys_.RegisterSensor(power_meter)

smoke_detector = Sensor("Smoke Detector", False)
sys_.RegisterSensor(smoke_detector)

# Setup initial action sets
# Configure sensor values
sys_.Process()  # Run the system once