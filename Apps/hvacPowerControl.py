from Apps.app import App


class HVACPowerControl(App):
    def __init__(self):
        App.__init__(self, "HVAC Power Control")

    def update(self, sys):
        return [], [], [], [], []
