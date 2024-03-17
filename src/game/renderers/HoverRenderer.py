from interfaces.IHoverable import IHoverable


class HoverRenderer:
    def __init__(self):
        self.hoverable_objects = []

    def register_hoverable_object(self, hoverable_object):
        if isinstance(hoverable_object, IHoverable):
            self.hoverable_objects.append(hoverable_object)

    def render_hover(self, mouse_pos, screen):
        self.hoverable_objects.sort(key=lambda obj: obj.get_hover_priority())
        for hoverable_object in self.hoverable_objects:
            if hoverable_object.is_hovered(mouse_pos):
                hoverable_object.render_hover(screen)
                break
