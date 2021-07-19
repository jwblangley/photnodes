import torch

from model.nodes.node import BaseNode


class SolidColorNode(BaseNode):
    def __init__(self):
        super().__init__()

    def check_requirements(self):
        return (
            hasattr(self, "color")
            and isinstance(self.color, torch.Tensor)
            and len(self.color.size()) == 1
            and self.color.size(0) == 3
            and hasattr(self, "width")
            and isinstance(self.width, int)
            and self.width > 0
            and hasattr(self, "height")
            and isinstance(self.height, int)
            and self.height > 0
        )

    def calculate(self, dependencies):
        res = torch.empty(3, self.height, self.width)
        res[0, :, :] = self.color[0]
        res[1, :, :] = self.color[1]
        res[2, :, :] = self.color[2]
        return res
