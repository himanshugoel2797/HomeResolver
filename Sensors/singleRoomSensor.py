from Sensors.sensor import Sensor


class SingleRoomSensor(Sensor):
    room_name = None

    def __init__(self, init_name, init_value, init_room_name):
        Sensor.__init__(self, init_name, init_value)
        self.room_name = init_room_name
