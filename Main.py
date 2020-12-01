#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cvxpy as cp
import numpy as np
import matplotlib.pyplot as plt
import math


# In[71]:


class Device:
    name = ""
    states = []  # List of state names
    state_changes = {}  
    resource_changes = {} # Nested dictionary describing how a given state transition affects global resources
    variables = {}  # Dictionary of device variables and their values
    current_state = None  # Current device state name

    def __init__(self, init_name, init_states, init_state_changes, init_variables, init_current_state):
        self.name = init_name
        self.states = init_states
        self.state_changes = init_state_changes
        self.variables = init_variables
        if init_current_state in self.states:
            self.current_state = init_current_state
        elif len(self.states) > 0:
            self.current_state = self.states[0]

    def TransitionState(self, target_state_name):
        if self.current_state != target_state_name and target_state_name in self.states:
            state_change = self.current_state + ":" + target_state_name
            for k, v in self.state_changes:
                if k == state_change:
                    # Use value.
                    break
            self.current_state = target_state_name

    # Set a variable's value
    def SetVariable(self, var_name, var_val):
        for k, v in self.variables.items():
            if k == var_name:
                v = var_val
                break
                
    def Update(self, sys, env):
        pass


class Sensor:
    name = ""
    value = None

    def __init__(self, init_name, init_value):
        self.name = init_name
        self.value = init_value

    def GetValue(self):
        return self.value


class App:
    name = ""

    def __init__(self, name):
        self.name = name
    
    # Process app functionality
    def Update(self, systemObj):
        pass


class Environment:
    temperature = 20
    time = 0 #in seconds
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
    electricity_rate = 0.115 / (60 * 60 * 1000) #$0.115/kWh to $/Ws
    electricity_rate_delta = 0
    
    def UpdateTemperature(self, delta):
        self.temp_delta += delta
    
    def UpdatePower(self, p):
        self.power_consumed_instant_delta += p
    
    def AddLight(self, l):
        self.light_delta += l
        
    def AddAmbientLight(self, l):
        self.ambient_light_delta += l
    
    def SetAmbientLightMult(self, m):
        self.ambient_light_mult = m
    
    def SetElectricityRate(self, r):
        self.electricity_rate_delta = r
        
    def UpdateUserDistance(self, d):
        self.user_distance_delta = d
    
    def Update(self):
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
        
        self.electricity_rate = 0.115 / (60 * 60 * 1000) * (1 + (0.5 * math.sin(self.time * math.pi / (12 * 60 * 60)) + 0.5) * 0.3)
        if self.electricity_rate != self.electricity_rate_delta:
            self.electricity_rate = self.electricity_rate_delta
        
        self.user_distance += self.user_distance_delta
        self.user_distance_delta = 0


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
    def RegisterDevice(self, obj):
        self.devices[obj.name] = obj

    # Name = string with sensor name
    # obj = object representing interface to sensor, implements Sensor class
    def RegisterSensor(self, obj):
        self.sensors[obj.name] = obj

    # Name = string with app name
    # obj = object representing instance of app, implements App class
    def RegisterApp(self, obj):
        self.apps[obj.name] = obj

    # Print current action set
    def ShowRunningSet(self):
        print("Current action set: " + self.action_set + "\n", end=",")

    # Run ILP
    # Update action set
    def Process(self):
        for app in self.apps.values():
            requested_actions, weights, mandatory_actions, alternative_action_pairs, exclusive_action_pairs = app.Update(self)

        tmp_action_set = self.action_set + requested_actions
        
        #Execute actions
        
        #Update all devices and sensors
        for dev in self.devices.values():
            dev.Update(self, self.env)
            
        for sense in self.sensors.values():
            sense.Update(self, self.env)
            
        self.time += 1
        self.rounded_time = self.time % (24 * 60 * 60)


# In[72]:


# Create and register devices and sensors
class HVAC(Device):
    temperature_curve = [0, 1 / (2 * 60), 1.3 / (2 * 60), 1.5 / (2 * 60), 2 / (2 * 60)] #Degrees change per second
    energy_curve = [0, 50, 125, 200, 300]
    def __init__(self):
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
            "rate": 1,
        }
        Device.__init__(self, "HVAC", states, state_changes, variables, "off")
    
    def GetResourceUsage(self, state_trans, variables):
        if state_trans.endswith("heating"):
            return {
                "power" : self.energy_curve[variables["rate"]] * 1.2,
                "temperature_delta" : self.temperature_curve[variables["rate"]],
            }
        elif state_trans.endswith("cooling"):
            return {
                "power" : self.energy_curve[variables["rate"]],
                "temperature_delta" : -self.temperature_curve[variables["rate"]],
            }
        else:
            return {
                "power" : 0,
                "temperature_delta" : 0,
            }
        
    def Update(self, sys, env):
        cur_vars = self.GetResourceUsage(self.current_state, self.variables)
        env.UpdatePower(cur_vars["power"]) #Consume power
        env.UpdateTemperature(cur_vars["temperature_delta"]) #Update current temperature


class Blind(Device):
    def __init__(self):
        states = ["raised", "lowered"]
        state_changes = {
            "raised:lowered": "Lower blinds requested",
            "lowered:raised": "Raise blinds requested",
        }
        variables = {
            "shutter_amount": 0
        }
        Device.__init__(self, "Blinds", states, state_changes, variables, "lowered")
        
    def GetResourceUsage(self, state_trans, variables):
        if state_trans.endswith("lowered"):
            return {
                "brightness_mult" : (4 - variables["shutter_amount"]) * 0.25,
            }
        elif state_trans.endswith("raised"):
            return {
                "brightness_mult" : 1,
            }
        else:
            return None
        
    def Update(self, sys, env):
        cur_vars = self.GetResourceUsage(self.current_state, self.variables)
        env.SetAmbientLightMult(cur_vars["brightness_mult"])


class IndoorLight(Device):
    def __init__(self, name):
        states = ["on", "off"]
        state_changes = {
            "off:on": "Lights on requested",
            "on:off": "Lights off requested",
        }
        Device.__init__(self, name, states, state_changes, {}, "off")
        
    def GetResourceUsage(self, state_trans, variables):
        if state_trans.endswith("on"):
            return {
                "brightness" : 1,
                "power" : 8.5,
            }
        elif state_trans.endswith("off"):
            return {
                "brightness" : 0,
                "power" : 0,
            }
        else:
            return None
        
    def Update(self, sys, env):
        cur_vars = self.GetResourceUsage(self.current_state, self.variables)
        env.UpdatePower(cur_vars["power"]) #Consume power
        env.AddLight(cur_vars["brightness"]) #Update light amount


class OutdoorLight(Device):
    def __init__(self, name):
        states = ["on", "off"]
        state_changes = {
            "off:on": "Lights on requested",
            "on:off": "Lights off requested",
        }
        variables = {
            "level": 0
        }
        Device.__init__(self, name, states, state_changes, variables, "off")
        
    def GetResourceUsage(self, state_trans, variables):
        if state_trans.endswith("on"):
            return {
                "brightness" : variables["level"] * 0.25,
                "power" : variables["level"] * 2.5,
            }
        elif state_trans.endswith("off"):
            return {
                "brightness" : 0,
                "power" : 0,
            }
        else:
            return None
        
    def Update(self, sys, env):
        cur_vars = self.GetResourceUsage(self.current_state, self.variables)
        env.UpdatePower(cur_vars["power"]) #Consume power
        env.AddLight(cur_vars["brightness"]) #Update light amount


class BatteryBackup(Device):
    def __init__(self):
        states = ["charging, supplying, idle"]
        state_changes = {
            "idle:charging": "Charging requested",
            "supplying:charging": "Charging requested",
            "idle:supplying": "Supplying requested",
            "charging:supplying": "Supplying requested",
            "charging:idle": "Idle requested",
            "supplying:idle": "Idle requested"
        }
        variables = {
            "stored" : 0,
            "consumption" : 0,
        }
        Device.__init__(self, "Battery Backup", states, state_changes, variables, "idle")
        
    def GetResourceUsage(self, state_trans, variables):
        return {
            "capacity" : 20000 * 60 * 60, #20kWh
            "charging_rate" : 1000, #1kW
        }
        
    def Update(self, sys, env):
        cur_vars = self.GetResourceUsage(self.current_state, self.variables)
        
        if self.current_state == "charging":
            env.UpdatePower(cur_vars["charging_rate"]) #Consume power
            self.variables["stored"] += cur_vars["charging_rate"]
            if self.variables["stored"] >= cur_vars["capacity"]: #Stop charging further
                self.variables["stored"] = cur_vars["capacity"]
                self.current_state = "idle"
        elif self.current_state == "supplying": #Supply as much power as available
            if self.variables["stored"] >= self.variables["consumption"]:
                self.variables["stored"] -= self.variables["consumption"]
                env.UpdatePower(-self.variables["consumption"])
            else:
                env.UpdatePower(-self.variables["stored"])
                self.variables["stored"] = 0
                self.current_state = "idle"


class Doors(Device):
    def __init__(self):
        states = ["opened", "closed"]
        state_changes = {
            "opened:closed": "Closed doors requested",
            "closed:opened": "Opened doors requested"
        }
        Device.__init__(self, "Doors", states, state_changes, {}, "closed")

    def GetResourceUsage(self, state_trans, variables):
        return {}

    def Update(self, sys, env):
        pass


# In[73]:


class Thermometer(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Thermometer", env.temperature)
    def Update(self, sys, env):
        self.value = env.temperature


class PresenceSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Presence Sensor", env.presence_detected)
    def Update(self, sys, env):
        self.value = env.presence_detected


class MotionSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Motion Sensor", env.motion_detected)
    def Update(self, sys, env):
        self.value = env.motion_detected


class PowerMeter(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Power Meter", env.power_consumed_instant)
    def Update(self, sys, env):
        self.value = env.power_consumed_instant


class PowerRate(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Power Rate", env.electricity_rate)
    def Update(self, sys, env):
        self.value = env.electricity_rate


class UserLocator(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "User Locator", env.user_distance)
    def Update(self, sys, env):
        self.value = env.user_distance


class IndoorBrightnessSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Indoor Brightness Sensor", env.light + env.ambient_light * env.ambient_light_mult)
    def Update(self, sys, env):
        self.value = env.light + env.ambient_light * env.ambient_light_mult


class OutdoorBrightnessSensor(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Outdoor Brightness Sensor", env.ambient_light)
    def Update(self, sys, env):
        self.value = env.ambient_light


class SmokeDetector(Sensor):
    def __init__(self, env):
        Sensor.__init__(self, "Smoke Detector", env.smoke_detected)
    def Update(self, sys, env):
        self.value = env.smoke_detected


# In[74]:


class SleepCycleManager(App):
    current_state = "sleep_pending"
    transition_counter = 0 #5 minutes
    def __init__(self, sleep_time, wake_time):
        App.__init__(self, "Sleep Cycle Manager")
        self.sleep_time = sleep_time
        self.wake_time = wake_time
        self.transition_time = 5
    def Update(self, sys):
        if self.current_state == "wake_pending" and sys.rounded_time >= self.wake_time:
            #Transition to wake mode
            self.current_state = "wake_processing"
            self.transition_counter = 0
        elif self.current_state == "wake_processing":
            #Set system to sleep pending
            self.transition_counter += 1
            #Slowly raise blinds
            if self.transition_counter == 1:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 2:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 3:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 4:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 5:
                self.current_state = "sleep_pending"
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
        elif self.current_state == "sleep_pending" and sys.rounded_time >= self.sleep_time:
            #Transition to sleep mode
            self.current_state = "sleep_processing"
            self.transition_counter = 0
        elif self.current_state == "sleep_processing":
            #Set system to wake pending
            self.transition_counter += 1
            #Slowly lower blinds
            if self.transition_counter == 1:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 2:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 3:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 4:
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
            elif self.transition_counter == 5:
                self.current_state = "sleep_pending"
                return ["""Submit requests to open all doors"""], [[0, 1, 10]], [0], [], []
        return [], [], [], [], []


class LightManager(App):
    current_state = "on_pending"
    def __init__(self, sunset_time, sunrise_time):
        App.__init__(self, "Light Manager")
        self.sunset_time = sunset_time
        self.sunrise_time = sunrise_time
        self.time_on = self.sunrise_time - self.sunset_time
        if self.time_on < 0:
            self.time_on += 24 * 60 * 60
    def Update(self, sys):
        if self.current_state == "on_pending" and sys.rounded_time >= self.sunset_time:
            #Request lights on
            self.current_state = "off_pending"
            return [{"device":"Indoor Lights", "target":"on", "timeout":self.time_on, "timeout_target":"off"}], [[sys.devices["Indoor Lights"].GetResourceUsage("on", None)["power"], 8, 10]], [], [], []
        elif self.current_state == "off_pending" and sys.rounded_time >= self.sunrise_time:
            #Request lights off
            self.current_state = "on_pending"
        return [], [], [], [], []


class SleepSecurity(App):
    def __init__(self):
        App.__init__(self, "Sleep Security")
    def Update(self, sys):
        return [], [], [], [], []


class IntruderPrevention(App):
    current_state = "on_pending"
    def __init__(self, on_time, off_time):
        App.__init__(self, "Intruder Prevention")
        self.on_time = on_time
        self.off_time = off_time
    def Update(self, sys):
        if self.current_state == "on_pending" and sys.rounded_time >= self.on_time:
            #Request lights on or motion sensing
            self.current_state = "off_pending"
            self.transition_counter = 0
        elif self.current_state == "off_pending" and sys.rounded_time >= self.off_time:
            #Request lights off
            self.current_state = "on_pending"
            self.transition_counter = 0
        return [], [], [], [], []


class FakeActivity(App):
    def __init__(self):
        App.__init__(self, "Fake Activity")


class FireSafety(App):
    def __init__(self):
        App.__init__(self, "Sleep Cycle Manager")
    def Update(self, sys):
        if sys.sensors["Smoke Detector"].value:
            return [{"device":"Doors", "target":"closed", "timeout":-1}], [[0, 1, 10]], [0], [], [] #requested_actions, weight_sets, mandatory_actions, alternative_action_pairs, exclusive_action_pairs
        return [], [], [], [], []


class HVACLocationControl(App):
    def __init__(self, target_temp):
        App.__init__(self, "HVAC Location Control")
        self.target_temp = target_temp
    def Update(self, sys):
        #Compute distance vs target temperature time to determine target heating/cooling rate
        hvac_props_h = [sys.devices["HVAC"].GetResourceUsage("heating", {"rate" : x + 1}) for x in range(4)]
        hvac_props_c = [sys.devices["HVAC"].GetResourceUsage("cooling", {"rate" : x + 1}) for x in range(4)]
        
        actions = []
        weights = []
        alt_actions = []
        
        #assume walking speed
        time_avail = sys.sensors["User Locator"].GetValue() / 1.4 #m/s
        cur_temp = sys.sensors["Thermometer"].GetValue()
        if cur_temp > self.target_temp:
            #Cooling
            hvac_tot = [(cur_temp - self.target_temp) / hvac_props_c[x].temperature_delta for x in range(4)]
            
            
        elif cur_temp < self.target_temp:
            #Heating
            hvac_tot = [(cur_temp - self.target_temp) / hvac_props_h[x].temperature_delta for x in range(4)]
        
        return actions, weights, [], alt_actions, []


class EnergyManagement(App):
    #Track total energy bill
    #Apply strict power constraint based on that
    def __init__(self):
        App.__init__(self, "Energy Management")
    def Update(self, sys):
        return [], [], [], [], []


class BatteryBackupManagement(App):
    #Request optional charging when close to lowest
    #Offer to supply when close to highest
    def __init__(self):
        App.__init__(self, "Battery Backup Management")
    def Update(self, sys):
        return [], [], [], [], []


class HVACPowerControl(App):
    def __init__(self):
        App.__init__(self, "HVAC Power Control")
    def Update(self, sys):
        return [], [], [], [], []


class HVACWeatherManagement(App):
    def __init__(self):
        App.__init__(self, "HVAC Weather Management")
    def Update(self, sys):
        return [], [], [], [], []


# In[75]:


env = Environment()
sys_ = System(env)


# In[76]:


human_presence_sensor = PresenceSensor(env)
sys_.RegisterSensor(human_presence_sensor)

thermometer = Thermometer(env)
sys_.RegisterSensor(thermometer)

outdoor_motion_detector = MotionSensor(env)
sys_.RegisterSensor(outdoor_motion_detector)

power_meter = PowerMeter(env)
sys_.RegisterSensor(power_meter)

power_rate = PowerRate(env)
sys_.RegisterSensor(power_rate)

user_locator = UserLocator(env)
sys_.RegisterSensor(user_locator)

indoor_brightness = IndoorBrightnessSensor(env)
sys_.RegisterSensor(indoor_brightness)

outdoor_brightness = OutdoorBrightnessSensor(env)
sys_.RegisterSensor(outdoor_brightness)

smoke_detector = SmokeDetector(env)
sys_.RegisterSensor(smoke_detector)


# In[77]:


doors = Doors()
sys_.RegisterDevice(doors)
        
hvac = HVAC()
sys_.RegisterDevice(hvac)

blinds = Blind()
sys_.RegisterDevice(blinds)

lightsOutdoor = OutdoorLight("Outdoor Lights")
sys_.RegisterDevice(lightsOutdoor)

lightsIndoor = IndoorLight("Indoor Lights")
sys_.RegisterDevice(lightsIndoor)

batteryBackup = BatteryBackup()
sys_.RegisterDevice(batteryBackup)


# In[78]:


sleep_cycle = SleepCycleManager(0 * 60 * 60, 8 * 60 * 60)
sys_.RegisterApp(sleep_cycle)

light_man = LightManager(19 * 60 * 60, 5 * 60 * 60)
sys_.RegisterApp(light_man)

sleep_sec = SleepSecurity()
sys_.RegisterApp(sleep_sec)

intruder_prev = IntruderPrevention(20 * 60 * 60, 23 * 60 * 60)
sys_.RegisterApp(intruder_prev)

fire_safety = FireSafety()
sys_.RegisterApp(fire_safety)

hvac_loc = HVACLocationControl(20)
sys_.RegisterApp(hvac_loc)

energy_man = EnergyManagement()
sys_.RegisterApp(energy_man)

batt_backup_man = BatteryBackupManagement()
sys_.RegisterApp(batt_backup_man)

hvac_power = HVACPowerControl()
sys_.RegisterApp(hvac_power)

hvac_weather = HVACWeatherManagement()
sys_.RegisterApp(hvac_weather)


# In[ ]:





# In[79]:


# Setup initial action sets
# Configure initial sensor values

# Print initial action set
# Update loop of environment and system
# Trigger event and print action set
sys_.Process()  # Run the system once
# Print final action set


# In[ ]:




