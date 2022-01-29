import os


SPACING = 10
UNIT_HEIGHT = 5
UNIT_WIDTH = 5

DEFAULT_QT_MATERIAL_THEME = "neutral_dark.xml"


class _Theme:
    qt_material_theme = DEFAULT_QT_MATERIAL_THEME

    @property
    def palette(self):
        return {
            "primary": os.environ["QTMATERIAL_PRIMARYCOLOR"],
            "primary_light": os.environ["QTMATERIAL_PRIMARYLIGHTCOLOR"],
            "primary_text": os.environ["QTMATERIAL_PRIMARYTEXTCOLOR"],
            "secondary": os.environ["QTMATERIAL_SECONDARYCOLOR"],
            "secondary_light": os.environ["QTMATERIAL_SECONDARYLIGHTCOLOR"],
            "secondary_dark": os.environ["QTMATERIAL_SECONDARYDARKCOLOR"],
            "secondary_text": os.environ["QTMATERIAL_SECONDARYTEXTCOLOR"],
            "highlight": "#80deea",
        }

    def spacing(self, factor):
        return SPACING * factor

    def unit_height(self, factor):
        return UNIT_HEIGHT * factor

    def unit_width(self, factor):
        return UNIT_WIDTH * factor


theme = _Theme()
