import math


class DoorNode:
    door_open = False
    door_locked = False
    in_room = None
    out_room = None

    def __init__(self, in_room, out_room):
        self.door_open = False
        self.in_room = in_room
        self.out_room = out_room

    def open(self):
        self.door_open = True

    def close(self):
        self.door_open = False

    def lock(self):
        self.door_open = False
        self.door_locked = True

    def unlock(self):
        self.door_locked = False


class Room:
    temperature = 20
    time = 0  # in seconds
    temp_delta = 0
    light = 0
    light_delta = 0
    smoke_detected = False
    sleep_detected = False
    presence_detected = False
    ambient_light_mult = 1

    doors = {}  # Names of rooms the doors connect to
    windows = []  # List of windows

    def __init__(self, name, env):
        self.name = name
        self.env = env

    def add_door(self, tgt_room_name, door):
        self.doors[tgt_room_name] = door

    def has_window(self):
        return len(self.windows) > 0

    def open_window(self):
        if len(self.windows) > 0:
            self.windows[0] = True

    def close_window(self):
        if len(self.windows) > 0:
            self.windows[0] = False

    def add_window(self):
        self.windows.append(False)

    def set_ambient_light_mult(self, m):
        self.ambient_light_mult = m

    def update_temperature(self, delta):
        self.temp_delta += delta

    def add_light(self, l):
        self.light_delta += l

    def update(self):
        self.time += 1
        self.temperature += self.temp_delta
        self.temp_delta = 0

        # Normalize temperatures and lighting with outside state when windows open
        self.light = self.light_delta + self.env.ambient_light * self.ambient_light_mult
        self.light_delta = 0

        # TODO Gradually normalize temperatures between neighboring rooms when doors are open

class Environment:
    time = 0
    power_consumed_instant = 0
    power_consumed_instant_delta = 0
    electricity_rate_base = 0.115 / (60 * 60 * 1000)
    electricity_rate = 0.115 / (60 * 60 * 1000)  # $0.115/kWh to $/Ws
    electricity_rate_delta = 0
    ambient_light = 0
    ambient_light_delta = 0

    rooms = {}
    room_names = []
    doors = {}
    door_names = []

    presence_detected = False
    motion_detected = False

    def __init__(self):
        # Setup rooms, doors and windows
        bd0 = Room("bedroom0", self)
        bd0.add_window()
        
        bd1 = Room("bedroom1", self)
        bd1.add_window()
        
        ktch = Room("kitchen", self)
        ktch.add_window()

        bathroom = Room("bathroom", self)

        livingroom = Room("livingroom", self)
        livingroom.add_window()

        bd0_exit = DoorNode(bd0, livingroom)
        bd1_exit = DoorNode(bd1, livingroom)
        ktch_exit = DoorNode(ktch, livingroom)
        bathroom_exit = DoorNode(bathroom, livingroom)
        main_door = DoorNode(livingroom, None)

        bd0.add_door("livingroom", bd0_exit)
        bd1.add_door("livingroom", bd1_exit)
        ktch.add_door("livingroom", ktch_exit)
        bathroom.add_door("livingroom", bathroom_exit)

        livingroom.add_door("bedroom0", bd0_exit)
        livingroom.add_door("bedroom1", bd1_exit)
        livingroom.add_door("kitchen", ktch_exit)
        livingroom.add_door("bathroom", bathroom_exit)
        livingroom.add_door("exit", main_door)

        self.rooms["bedroom0"] = bd0
        self.rooms["bedroom1"] = bd1
        self.rooms["kitchen"] = ktch
        self.rooms["bathroom"] = bathroom
        self.rooms["livingroom"] = livingroom
        self.room_names = self.rooms.keys()

        self.doors["bedroom0"] = bd0_exit
        self.doors["bedroom1"] = bd1_exit
        self.doors["kitchen"] = ktch_exit
        self.doors["bathroom"] = bathroom_exit
        self.doors["exit"] = main_door
        self.door_names = self.doors.keys()

    def update_power(self, p):
        self.power_consumed_instant_delta += p

    def set_electricity_rate(self, r):
        self.electricity_rate_delta = r - self.electricity_rate

    def add_light(self, l):
        self.ambient_light_delta += l

    def update(self):
        self.time += 1
        self.power_consumed_instant = self.power_consumed_instant_delta
        self.power_consumed_instant_delta = 0

        self.ambient_light = 0.5 * \
            math.sin(self.time * math.pi / (12 * 60 * 60)) + 0.5
        self.ambient_light += self.ambient_light_delta
        self.ambient_light_delta = 0

        self.electricity_rate = self.electricity_rate_base * \
            (1 + (0.5 * math.sin(self.time * math.pi / (12 * 60 * 60)) + 0.5)
             * 0.3) + self.electricity_rate_delta

        self.presence_detected = False
        for r in self.rooms.values():
            r.update()
            if r.presence_detected:
                self.presence_detected = True
