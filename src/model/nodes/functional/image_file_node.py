import os

from model.nodes.node import BaseNode
from model.image_io.image_io_adapter import load_neutral_image


class ImageFileNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.path = None
        self.gamma_decode = None

        self._path_dirty = True
        self._raw_img_cache = None

    def set_attribute(self, name, value):
        if name == "path":
            self._path_dirty = True

        return super().set_attribute(name, value)

    def check_requirements(self, dependencies):
        return (
            isinstance(self.path, str)
            and os.path.isfile(self.path)
            and isinstance(self.gamma_decode, float)
        )

    def calculate(self, dependencies):
        if self._path_dirty:
            self._raw_img_cache = load_neutral_image(self.path)
            self._path_dirty = False

        return self._raw_img_cache

        # Gamma decoding
        # return res.pow(dependencies["gamma"])
