from Apps.app import App


class EnergyManagement(App):
    # Track total energy bill
    # Apply strict power constraint based on that
    def __init__(self):
        App.__init__(self, "Energy Management")

    def update(self, sys):
        return [], [], [], [], []
