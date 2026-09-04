class EventBus:
    def __init__(self) -> None:
        self._handlers = []

    def subscribe(self, handler) -> None:
        self._handlers.append(handler)

    def publish(self, event) -> None:
        for handler in self._handlers:
            handler(event)
