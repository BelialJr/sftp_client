import traceback

from PyQt5.QtWidgets import QMenu, QApplication


class ThemeView:
    menuView: QMenu = None
    menuViewAction = None
    app = None
    default_theme = 'Light Theme'
    current_theme = None
    theme_to_filePath = {'Light Theme': '../stylesheets/light_stylesheet.qss',
                         'Dark Theme': '../stylesheets/dark_stylesheet.qss'}
    theme_to_stylesheet = {}
    theme_to_action = {}

    @classmethod
    def get_current_style_sheet(cls):
        return cls.theme_to_stylesheet[cls.current_theme]

    @classmethod
    def set_menu(cls, menu: QMenu, app):
        cls.menuView = menu
        cls.app = app
        for key, val in cls.theme_to_filePath.items():
            cls.add_action(key)
        cls.set_current_theme('Light Theme')

    @classmethod
    def set_action_checked(cls, action):
        for a in cls.theme_to_action.values():
            a.setChecked(False)
        action.setChecked(True)

    @classmethod
    def set_current_theme(cls, themeName):
        cls.current_theme = themeName
        cls.set_action_checked(cls.theme_to_action[themeName])
        stylesheet_text = cls.theme_to_stylesheet.get(themeName)
        if stylesheet_text:
            cls.app.setStyleSheet(cls.theme_to_stylesheet.get(themeName))
        else:
            try:
                qss_file = open(cls.theme_to_filePath[themeName]).read()
                cls.theme_to_stylesheet.update({themeName: qss_file})
                cls.app.setStyleSheet(qss_file)
            except Exception:
                traceback.print_exc()

    # print(PyQt5.QtWidgets.QStyleFactory.keys())
    # app.setStyle('Fusion')

    @classmethod
    def add_action(cls, key):
        action = cls.menuView.addAction(key, lambda: (
            cls.set_current_theme(key)
        ))
        action.setCheckable(True)
        cls.theme_to_action.update({key: action})
