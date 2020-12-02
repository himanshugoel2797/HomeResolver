class System:
    devices = {}
    sensors = {}
    apps = {}
    resources = ['power_cost', 'comfort', 'security']
    time = 0
    rounded_time = 0
    action_set = []

    def __init__(self, env):
        self.env = env

    # Name = string with device name
    # Obj = object representing interface to device, implements Device class
    def register_device(self, obj):
        self.devices[obj.name] = obj

    # Name = string with sensor name
    # obj = object representing interface to sensor, implements Sensor class
    def register_sensor(self, obj):
        self.sensors[obj.name] = obj

    # Name = string with app name
    # obj = object representing instance of app, implements App class
    def register_app(self, obj):
        self.apps[obj.name] = obj

    # Print current action set
    def show_running_set(self):
        print("Current action set: " + self.action_set + "\n", end=",")

    # Run ILP
    # Update action set
    def process(self):
        requested_actions = []
        for app in self.apps.values():
            requested_actions, weights, mandatory_actions, alternative_action_pairs, exclusive_action_pairs =\
                app.update(self)

        tmp_action_set = self.action_set + requested_actions

        # Execute actions

        # Update all devices and sensors
        for dev in self.devices.values():
            dev.update(self, self.env)

        for sense in self.sensors.values():
            sense.update(self, self.env)

        self.time += 1
        self.rounded_time = self.time % (24 * 60 * 60)
