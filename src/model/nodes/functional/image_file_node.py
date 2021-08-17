import os

from model.nodes.node import BaseNode
from model.image_io.image_io_adapter import load_neutral_image
from model.nodes.node_process_error import NodeProcessError


class ImageFileNode(BaseNode):
    REQUIRES_GAMMA_CONNECTION = False

    def __init__(self):
        super().__init__()
        self.path = None

    def check_requirements(self, dependencies):
        if not isinstance(self.path, str):
            raise NodeProcessError(self, "path is not a string")
        if not os.path.isfile(self.path):
            raise NodeProcessError(self, "supplied path does not point to a file")

    def calculate(self, dependencies):
        return load_neutral_image(self.path)
