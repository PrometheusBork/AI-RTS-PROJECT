from interfaces import IHoverable


class HoverObserver:
    _instance = None
    _hoverable_tiles = []
    _hoverable_objects = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Separate method won't scale well
    def register_tile(self, hoverable: IHoverable):
        self._hoverable_tiles.append(hoverable)

    def register_objects(self, hoverable: IHoverable):
        self._hoverable_objects.append(hoverable)

    def notify(self, mouse_pos, screen):
        for hoverable in self._hoverable_objects:
            if hoverable.is_hovered(mouse_pos):
                hoverable.render_hover(screen)
                return

        for hoverable in self._hoverable_tiles:
            if hoverable.is_hovered(mouse_pos):
                hoverable.render_hover(screen)

    def clear_observers(self):
        self._hoverable_tiles.clear()
        self._hoverable_objects.clear()
