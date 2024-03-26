from game.gui.menus.MainMenu import MainMenu
from game.gui.menus.OptionMenu import OptionMenu
from game.gui.menus.NewGameMenu import NewGameMenu

class MenuManager:
    def __init__(self, screen_size, state_manager):
        self.screen_size = screen_size
        self.state_manager = state_manager
        self.active_menu = None
        self.menus = {}
        self.register_menu("menu", MainMenu(self.screen_size, self))
        self.register_menu("option", OptionMenu(self.screen_size, self))
        self.register_menu("new_game", NewGameMenu(self.screen_size, self))
        self.activate_menu("menu")

    def register_menu(self, menu_id, gui_menu):
        self.menus[menu_id] = gui_menu

    def activate_menu(self, menu_id):
        self.active_menu = self.menus.get(menu_id)

    def deactivate_menu(self):
        self.active_menu = None

    def is_menu_active(self):
        return self.active_menu is not None

    def process_events(self, events):
        if self.active_menu:
            self.active_menu.process_events(events)

    def render(self, surface):
        if self.active_menu:
            self.active_menu.render(surface)
