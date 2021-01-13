#!/usr/bin/env python36
# coding: utf-8


from Devices.batteryBackup import BatteryBackup
from Devices.blind import Blind
from Devices.door import Door
from Devices.hvac import HVAC
from Devices.indoorLight import IndoorLight
from Devices.outdoorLight import OutdoorLight
from Devices.window import Window

from Sensors.indoorBrightnessSensor import IndoorBrightnessSensor
from Sensors.motionSensor import MotionSensor
from Sensors.outdoorBrightnessSensor import OutdoorBrightnessSensor
from Sensors.powerMeter import PowerMeter
from Sensors.powerRate import PowerRate
from Sensors.presenceSensor import PresenceSensor
from Sensors.sleepSensor import SleepSensor
from Sensors.smokeDetector import SmokeDetector
from Sensors.thermometer import Thermometer
from Sensors.userLocator import UserLocator

from Apps.batteryBackupManagement import BatteryBackupManagement
from Apps.energyManagement import EnergyManagement
from Apps.fakeActivity import FakeActivity
from Apps.fireSafety import FireSafety
from Apps.hvacLocationControl import HVACLocationControl
from Apps.hvacPowerControl import HVACPowerControl
from Apps.intruderPrevention import IntruderPrevention
from Apps.lightManager import LightManager
from Apps.sleepCycleManager import SleepCycleManager
from Apps.sleepSecurity import SleepSecurity

from environment import Environment

from system import System


def update():
    env.update()
    sys_.process()

    sys_.show_current_state()


env = Environment()
sys_ = System(env)

# # # # # SENSORS # # # # #
outdoor_motion_detector = MotionSensor(env)
sys_.register_sensor(outdoor_motion_detector)

power_meter = PowerMeter(env)
sys_.register_sensor(power_meter)

power_rate = PowerRate(env)
sys_.register_sensor(power_rate)

user_locator = UserLocator(env)
sys_.register_sensor(user_locator)

outdoor_brightness = OutdoorBrightnessSensor(env)
sys_.register_sensor(outdoor_brightness)

human_presence_sensor = PresenceSensor(env)
sys_.register_sensor(human_presence_sensor)

for room_name in env.room_names:
    indoor_brightness = IndoorBrightnessSensor(env, room_name)
    sys_.register_sensor(indoor_brightness)

    smoke_detector = SmokeDetector(env, room_name)
    sys_.register_sensor(smoke_detector)

    thermometer = Thermometer(env, room_name)
    sys_.register_sensor(thermometer)

    if room_name.startswith("bedroom"):
        sleep_detector = SleepSensor(env, room_name)
        sys_.register_sensor(sleep_detector)

# # # # # DEVICES # # # # #

for door_name in env.door_names:
    door = Door(door_name)
    sys_.register_device(door)

for room_name in env.room_names:
    lightsIndoor = IndoorLight(room_name)
    sys_.register_device(lightsIndoor)

    hvac = HVAC(room_name)
    sys_.register_device(hvac)

    if env.rooms[room_name].has_window():
        windows = Window(room_name)
        sys_.register_device(windows)

        blinds = Blind(room_name)
        sys_.register_device(blinds)

lightsOutdoor = OutdoorLight("Outdoor Lights")
sys_.register_device(lightsOutdoor)

batteryBackup = BatteryBackup()
sys_.register_device(batteryBackup)

# # # # # APPS # # # # #

batt_backup_man = BatteryBackupManagement(
    0.15 / (60 * 60 * 1000), 0.2 / (60 * 60 * 1000))
sys_.register_app(batt_backup_man)

# Keep total bill under $100, never allow instantaneous power to be greater than $120
energy_man = EnergyManagement(100, 120 / (30 * 24 * 60 * 60))
sys_.register_app(energy_man)

fake_act = FakeActivity(6 * 60 * 60, 22 * 60 * 60, 15 * 60, 15 * 60)
sys_.register_app(fake_act)

fire_safety = FireSafety()
sys_.register_app(fire_safety)

hvac_loc = HVACLocationControl()
sys_.register_app(hvac_loc)

hvac_power = HVACPowerControl()
sys_.register_app(hvac_power)

intruder_prev = IntruderPrevention(0 * 60 * 60, 3 * 60 * 60)
sys_.register_app(intruder_prev)

light_man = LightManager(19 * 60 * 60, 5 * 60 * 60)
sys_.register_app(light_man)

sleep_cycle = SleepCycleManager(0 * 60 * 60, 8 * 60 * 60)
sys_.register_app(sleep_cycle)

sleep_sec = SleepSecurity()
sys_.register_app(sleep_sec)

# # # # # SIMULATION # # # # #

sys_.show_current_state()

env.presence_detected = True
env.temperature = 40
env.user_location = "Out of the House"

update()
