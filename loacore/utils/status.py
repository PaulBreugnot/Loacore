
class ProcessState:

    def __init__(self, pid, activity, progress):
        self.pid = pid
        self.activity = activity
        self.progress = progress

    def state_str(self):
        return str(self.pid) + "\t" + self.activity + "\t" + str(self.progress) + "%"
