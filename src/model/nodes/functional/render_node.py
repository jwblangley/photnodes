import torch

from model.nodes.node import BaseNode


class _GammaNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.gamma = None

    def check_requirements(self, dependencies):
        return isinstance(self.gamma, float) and self.gamma > 0

    def calculate(self, dependencies):
        return self.gamma


class RenderNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.gamma = None

        self._gamma_node = _GammaNode()

    @staticmethod
    def encode_gamma(img, gamma):
        return img.pow(1 / gamma)

    def set_attribute(self, name, value):
        if name == "gamma" and value is not None:
            self._gamma_node.set_attribute("gamma", value)

        return super().set_attribute(name, value)

    def check_requirements(self, dependencies):
        return (
            isinstance(self.gamma, float)
            and self.gamma > 0
            and "_primary_in" in dependencies
            and isinstance(dependencies["_primary_in"], torch.Tensor)
        )

    def calculate(self, dependencies):
        # Apply gamma encoding
        if dependencies["_primary_in"] is None:
            return None

        return RenderNode.encode_gamma(dependencies["_primary_in"], self.gamma)
