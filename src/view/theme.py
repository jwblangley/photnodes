import qt_material


SPACING = 10

DEFAULT_QT_MATERIAL_THEME = "neutral_dark.xml"


class _Theme:
    qt_material_theme = DEFAULT_QT_MATERIAL_THEME

    def spacing(self, factor):
        return SPACING * factor


theme = _Theme()
