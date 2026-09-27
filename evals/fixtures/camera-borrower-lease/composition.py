class CameraPort:
    def __init__(self):
        self.open = False

    def connect(self):
        self.open = True

    def close(self):
        self.open = False

    def read_frame(self):
        if not self.open:
            raise RuntimeError("camera disconnected")
        return b"frame"


class PreviewSession:
    def __init__(self, camera):
        self.camera = camera
        self.paused = False

    def start(self):
        self.camera.connect()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False
        return self.camera.read_frame()

    def close(self):
        self.camera.close()


class FrameSubscription:
    def __init__(self, camera):
        self.camera = camera
        self.active = False

    def start(self):
        self.active = True

    def pause(self):
        self.active = False

    def resume(self):
        self.active = True

    def close(self):
        self.active = False


class FrameAnalysis:
    def __init__(self, camera):
        self.camera = camera
        self.subscription = FrameSubscription(camera)

    def start(self):
        self.subscription.start()
        return self.camera.read_frame()

    def pause(self):
        self.subscription.pause()

    def resume(self):
        self.subscription.resume()
        return self.camera.read_frame()

    def close(self):
        self.subscription.close()
        self.camera.close()


def inspect_preview_lifecycle(preview):
    analysis = FrameAnalysis(preview.camera)
    analysis.start()
    analysis.pause()
    analysis.resume()
    analysis.close()
    preview.resume()
    return FrameAnalysis(preview.camera).start()
