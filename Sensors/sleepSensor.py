from Sensors.sensor import Sensor

class SleepSensor(Sensor):
    room_name = None
    def __init__(self, env, room_name):
        Sensor.__init__(self, "Sleep Sensor_%s" % (room_name), env.rooms[room_name].sleep_detected)
        self.room_name = room_name

    def update(self, sys, env):
        self.value = env.rooms[self.room_name].sleep_detected
