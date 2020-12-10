from Apps.app import App


class HVACWeatherManagement(App):
    def __init__(self):
        App.__init__(self, "HVAC Weather Management")

    def update(self, sys):
        return [], [], [], [], [], []
