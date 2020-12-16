class App:
    name = ""

    @staticmethod
    def app_print(msg):
        BLUE = '\033[94m'  # ANSI color code for blue
        END = '\033[0m'
        print(BLUE + msg + END)

    def __init__(self, name):
        self.name = name

    # Process app functionality
    def update(self, system_obj):
        return [], [], [], [], [], []
