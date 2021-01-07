from Sensors.sensor import Sensor


class Thermometer(Sensor):
    room_name = None
    def __init__(self, env, room_name):
        Sensor.__init__(self, "Thermometer_%s"%(room_name), env.rooms[room_name].temperature)
        self.room_name = room_name

    def update(self, sys, env):
        self.value = env.rooms[self.room_name].temperature
