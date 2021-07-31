import torch

from model.nodes.node import BaseNode


class SolidColorNode(BaseNode):
    REQUIRES_GAMMA_CONNECTION = True

    def __init__(self):
        super().__init__()
        self.color = None
        self.width = None
        self.height = None

    def check_requirements(self, dependencies):
        return (
            isinstance(self.color, torch.Tensor)
            and len(self.color.size()) == 1
            and self.color.size(0) == 3
            and isinstance(self.width, int)
            and self.width > 0
            and isinstance(self.height, int)
            and self.height > 0
            and "gamma" in dependencies
            and isinstance(dependencies["gamma"], float)
        )

    def calculate(self, dependencies):
        res = torch.empty(3, self.height, self.width)
        res[0, :, :] = self.color[0]
        res[1, :, :] = self.color[1]
        res[2, :, :] = self.color[2]

        # Gamma decoding
        return res.pow(dependencies["gamma"])
