import math


class Environment:
    temperature = 20
    time = 0  # in seconds
    temp_delta = 0
    ambient_light = 0
    ambient_light_delta = 0
    ambient_light_mult = 1
    light = 0
    light_delta = 0
    power_consumed_instant = 0
    power_consumed_instant_delta = 0
    presence_detected = False
    motion_detected = False
    smoke_detected = False
    sleep_detected = False
    user_distance = 0
    user_distance_delta = 0
    electricity_rate_base = 0.115 / (60 * 60 * 1000)
    electricity_rate = 0.115 / (60 * 60 * 1000)  # $0.115/kWh to $/Ws
    electricity_rate_delta = 0

    def update_temperature(self, delta):
        self.temp_delta += delta

    def update_power(self, p):
        self.power_consumed_instant_delta += p

    def add_light(self, l):
        self.light_delta += l

    def add_ambient_light(self, l):
        self.ambient_light_delta += l

    def set_ambient_light_mult(self, m):
        self.ambient_light_mult = m

    def set_electricity_rate(self, r):
        self.electricity_rate_delta = r

    def update_user_distance(self, d):
        self.user_distance_delta = d

    def update(self):
        self.time += 1
        self.temperature += self.temp_delta
        self.temp_delta = 0

        self.power_consumed_instant = self.power_consumed_instant_delta
        self.power_consumed_instant_delta = 0

        self.light = self.light_delta
        self.light_delta = 0

        self.ambient_light = 0.5 * math.sin(self.time * math.pi / (12 * 60 * 60)) + 0.5
        self.ambient_light += self.ambient_light_delta
        self.ambient_light_delta = 0

        self.ambient_light_mult = 1

        self.electricity_rate = self.electricity_rate_base * \
                                (1 + (0.5 * math.sin(self.time * math.pi / (12 * 60 * 60)) + 0.5) * 0.3)
        
        self.user_distance += self.user_distance_delta
        self.user_distance_delta = 0
