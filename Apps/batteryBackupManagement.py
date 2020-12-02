from Apps.app import App


class BatteryBackupManagement(App):
    # Request optional charging when close to lowest
    # Offer to supply when close to highest
    def __init__(self):
        App.__init__(self, "Battery Backup Management")

    def update(self, sys):
        return [], [], [], [], []
