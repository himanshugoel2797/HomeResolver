class Sensor:
    name = ""
    value = None

    def __init__(self, init_name, init_value):
        self.name = init_name
        self.value = init_value

    def get_value(self):
        return self.value
