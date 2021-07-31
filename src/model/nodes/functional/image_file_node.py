import os

from model.nodes.node import BaseNode
from model.image_io.image_io_adapter import load_neutral_image


class ImageFileNode(BaseNode):
    REQUIRES_GAMMA_CONNECTION = False

    def __init__(self):
        super().__init__()
        self.path = None
        self.gamma_decode = None

    def check_requirements(self, dependencies):
        return (
            isinstance(self.path, str)
            and os.path.isfile(self.path)
            and isinstance(self.gamma_decode, float)
        )

    def calculate(self, dependencies):
        return load_neutral_image(self.path, self.gamma_decode)
