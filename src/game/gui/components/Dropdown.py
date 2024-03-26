import pygame_gui

class Dropdown(pygame_gui.elements.UIDropDownMenu):
    def __init__(self, options_list, starting_option, relative_rect, manager=None, container=None, parent_element=None, object_id=None, expansion_height_limit=None, anchors=None, visible=1, expand_on_option_click=True, on_selection=None):
        super().__init__(
            options_list=options_list,
            starting_option=starting_option,
            relative_rect=relative_rect,
            manager=manager,
            container=container,
            parent_element=parent_element,
            object_id=object_id,
            expansion_height_limit=expansion_height_limit,
            anchors=anchors,
            visible=visible,
            expand_on_option_click=expand_on_option_click
        )
        self.set_selection_callback(on_selection)

    def drop_down_menu_changed(self, text, selected_option):
        if self._on_selection_callback:
            self._on_selection_callback(selected_option)

    def set_selection_callback(self, callback):
        self._on_selection_callback = callback
