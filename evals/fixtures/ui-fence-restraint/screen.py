class AccountFence:
    def __init__(self):
        self.epoch = 0
        self.visible = None

    def switch(self):
        self.epoch += 1
        self.visible = None

    def publish_if_current(self, epoch, result):
        if epoch != self.epoch:
            return False
        self.visible = result
        return True


async def load_screen(fence, service):
    epoch = fence.epoch
    result = await service.read()
    fence.visible = result
