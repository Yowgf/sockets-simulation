class TerminateServer(Exception):
    def __init__(self, reason):
        super().__init__("Terminating server due to reason: " + reason)
