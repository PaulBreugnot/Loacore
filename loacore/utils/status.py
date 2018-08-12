
class ProcessState:

    def __init__(self, id_process, pid, activity, progress):
        self.id_process = id_process
        self.pid = pid
        self.activity = activity
        self.progress = progress

    def state_str(self):
        return ["[process " + str(self.id_process) + "]", str(self.pid), self.activity, self.progress]
