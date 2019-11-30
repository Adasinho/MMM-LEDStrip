class MotionSensorController:
    def __init__(self):
        self.motionStatus = False
        self.triggered = False

    def get_motion_status(self):
        import sensors_configuration
        return sensors_configuration.get_actual_motion_status()

    def update(self):
        actual_motion_status = self.get_motion_status()
        if self.motionStatus != actual_motion_status:
            self.motionStatus = actual_motion_status

            if self.motionStatus:
                print("Somebody is here!")
                self.triggered = True
            else:
                print("Nobody is here!")
        else:
            self.triggered = False

    def check_if_triggered(self):
        if self.triggered:
            self.triggered = False
            return True
        else:
            return False
