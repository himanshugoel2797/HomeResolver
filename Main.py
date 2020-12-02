#!/usr/bin/env python
# coding: utf-8

# In[1]:

from Devices.hvac import HVAC
from Devices.blind import Blind
from Devices.indoorLight import IndoorLight
from Devices.outdoorLight import OutdoorLight
from Devices.batteryBackup import BatteryBackup
from Devices.doors import Doors
from Sensors.thermometer import Thermometer
from Sensors.presenceSensor import PresenceSensor
from Sensors.motionSensor import MotionSensor
from Sensors.powerMeter import PowerMeter
from Sensors.powerRate import PowerRate
from Sensors.userLocator import UserLocator
from Sensors.indoorBrightnessSensor import IndoorBrightnessSensor
from Sensors.outdoorBrightnessSensor import OutdoorBrightnessSensor
from Sensors.smokeDetector import SmokeDetector
from Apps.sleepCycleManager import SleepCycleManager
from Apps.lightManager import LightManager
from Apps.sleepSecurity import SleepSecurity
from Apps.intruderPrevention import IntruderPrevention
from Apps.fakeActivity import FakeActivity
from Apps.fireSafety import FireSafety
from Apps.hvacLocationControl import HVACLocationControl
from Apps.energyManagement import EnergyManagement
from Apps.batteryBackupManagement import BatteryBackupManagement
from Apps.hvacPowerControl import HVACPowerControl
from Apps.hvacWeatherManagement import HVACWeatherManagement
from environment import Environment
from system import System

# In[71]:


# In[72]:


# Create and register devices and sensors


# In[73]:


# In[74]:


# In[75]:


env = Environment()
sys_ = System(env)


# In[76]:


human_presence_sensor = PresenceSensor(env)
sys_.register_sensor(human_presence_sensor)

thermometer = Thermometer(env)
sys_.register_sensor(thermometer)

outdoor_motion_detector = MotionSensor(env)
sys_.register_sensor(outdoor_motion_detector)

power_meter = PowerMeter(env)
sys_.register_sensor(power_meter)

power_rate = PowerRate(env)
sys_.register_sensor(power_rate)

user_locator = UserLocator(env)
sys_.register_sensor(user_locator)

indoor_brightness = IndoorBrightnessSensor(env)
sys_.register_sensor(indoor_brightness)

outdoor_brightness = OutdoorBrightnessSensor(env)
sys_.register_sensor(outdoor_brightness)

smoke_detector = SmokeDetector(env)
sys_.register_sensor(smoke_detector)


# In[77]:


doors = Doors()
sys_.register_device(doors)
        
hvac = HVAC()
sys_.register_device(hvac)

blinds = Blind()
sys_.register_device(blinds)

lightsOutdoor = OutdoorLight("Outdoor Lights")
sys_.register_device(lightsOutdoor)

lightsIndoor = IndoorLight("Indoor Lights")
sys_.register_device(lightsIndoor)

batteryBackup = BatteryBackup()
sys_.register_device(batteryBackup)


# In[78]:


sleep_cycle = SleepCycleManager(0 * 60 * 60, 8 * 60 * 60)
sys_.register_app(sleep_cycle)

light_man = LightManager(19 * 60 * 60, 5 * 60 * 60)
sys_.register_app(light_man)

sleep_sec = SleepSecurity()
sys_.register_app(sleep_sec)

intruder_prev = IntruderPrevention(20 * 60 * 60, 23 * 60 * 60)
sys_.register_app(intruder_prev)

fake_act = FakeActivity()
sys_.register_app(fake_act)

fire_safety = FireSafety()
sys_.register_app(fire_safety)

hvac_loc = HVACLocationControl(20)
sys_.register_app(hvac_loc)

energy_man = EnergyManagement()
sys_.register_app(energy_man)

batt_backup_man = BatteryBackupManagement()
sys_.register_app(batt_backup_man)

hvac_power = HVACPowerControl()
sys_.register_app(hvac_power)

hvac_weather = HVACWeatherManagement()
sys_.register_app(hvac_weather)


# In[ ]:


# In[79]:


# Setup initial action sets
# Configure initial sensor values

# Print initial action set
# Update loop of environment and system
# Trigger event and print action set
sys_.process()  # Run the system once
# Print final action set


# In[ ]:
