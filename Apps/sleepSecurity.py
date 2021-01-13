from Apps.app import App


class SleepSecurity(App):
    def __init__(self):
        App.__init__(self, "Sleep Security")

    def update(self, sys):
        sleep_sensors = sys.all_sensors_of_type("Sleep Sensor_")
        for i in range(len(sleep_sensors)):
            if not sys.sensors[sleep_sensors[i]].value:
                App.app_print("[Sleep Security] [Doors] Doors closed requested")
                return [{"device": "Door_%s" % sleep_sensors[i][13:], "target": "closed"}], [[0, 9, 10]], [], [], [], []
        return [], [], [], [], [], []
