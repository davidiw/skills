class Camera:
    def __init__(self):
        self.open = True

    def close(self):
        self.open = False


class Preview:
    def __init__(self, camera):
        self.camera = camera

    def handoff(self):
        return self.camera


class Recording:
    def __init__(self, camera):
        self.camera = camera

    def finish(self):
        self.camera.close()
