import torch

from model.nodes.node import BaseNode


class SolidColorNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.color = None
        self.width = None
        self.height = None

    def check_requirements(self):
        return (
            isinstance(self.color, torch.Tensor)
            and len(self.color.size()) == 1
            and self.color.size(0) == 3
            and isinstance(self.width, int)
            and self.width > 0
            and isinstance(self.height, int)
            and self.height > 0
            and "gamma" in self.input_connections
        )

    def calculate(self, dependencies):
        res = torch.empty(3, self.height, self.width)
        res[0, :, :] = self.color[0]
        res[1, :, :] = self.color[1]
        res[2, :, :] = self.color[2]

        # Gamma decoding
        return res.pow(dependencies["gamma"])
