import torch

from model.nodes.node import BaseNode
from model.nodes.node_process_error import NodeProcessError


class SolidColorNode(BaseNode):
    REQUIRES_GAMMA_CONNECTION = True

    def __init__(self):
        super().__init__()
        self.color = None
        self.width = None
        self.height = None

    def check_requirements(self, dependencies):
        if not isinstance(self.color, torch.Tensor):
            raise NodeProcessError(self, "color is not a tensor")
        if len(self.color.size()) != 1:
            raise NodeProcessError(self, "color does not have one dimension")
        if self.color.size(0) != 3:
            raise NodeProcessError(self, "color does not have three channels")
        if not isinstance(self.width, int):
            raise NodeProcessError(self, "width is not an integer")
        if self.width <= 0:
            raise NodeProcessError(self, "width is not positive")
        if not isinstance(self.height, int):
            raise NodeProcessError(self, "height is not an integer")
        if self.height <= 0:
            raise NodeProcessError(self, "height is not positive")
        if "gamma" not in dependencies:
            raise NodeProcessError(self, "gamma dependency is not provided")
        if not isinstance(dependencies["gamma"], float):
            raise NodeProcessError(
                self, "gamma dependency is not a floating point number"
            )

    def calculate(self, dependencies):
        res = torch.empty(3, self.height, self.width)
        res[0, :, :] = self.color[0]
        res[1, :, :] = self.color[1]
        res[2, :, :] = self.color[2]

        # Gamma decoding
        return res.pow(dependencies["gamma"])
