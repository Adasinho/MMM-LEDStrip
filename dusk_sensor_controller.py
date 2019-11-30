class DuskSensorController:
    def __init__(self):
        self.light_status = False
        self.triggered = False

    def get_dusk_status(self):
        import sensors_configuration
        return sensors_configuration.get_actual_light_status()

    def update(self):
        actual_light_status = self.get_dusk_status()
        if self.light_status != actual_light_status:
            self.light_status = actual_light_status
            self.triggered = True
        else:
            self.triggered = False

    def check_if_triggered(self):
        if self.triggered:
            self.triggered = False
            return True
        else:
            return False

    def get_light_status(self):
        return self.light_status
