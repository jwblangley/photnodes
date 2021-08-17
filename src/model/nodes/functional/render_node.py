import torch

from model.nodes.node import BaseNode
from model.nodes.node_process_error import NodeProcessError


class _GammaNode(BaseNode):
    REQUIRES_GAMMA_CONNECTION = False

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.gamma = None

    def check_requirements(self, dependencies):
        if not isinstance(self.gamma, float):
            raise NodeProcessError(self.parent, "gamma is not a floating point number")
        if self.gamma <= 0:
            raise NodeProcessError(self.parent, "gamma is not a positive number")

    def calculate(self, dependencies):
        return self.gamma


class RenderNode(BaseNode):
    REQUIRES_GAMMA_CONNECTION = False

    def __init__(self):
        super().__init__()
        self.gamma = None

        self._gamma_node = _GammaNode(self)

    @staticmethod
    def encode_gamma(img, gamma):
        return img.pow(1 / gamma)

    def set_attribute(self, name, value):
        if name == "gamma" and value is not None:
            self._gamma_node.set_attribute("gamma", value)

        return super().set_attribute(name, value)

    def check_requirements(self, dependencies):
        if not isinstance(self.gamma, float):
            raise NodeProcessError(self, "gamma is not a floating point number")
        if self.gamma <= 0:
            raise NodeProcessError(self, "gamma is not a positive number")
        if "_primary_in" not in dependencies:
            raise NodeProcessError(self, "primary input is not provided")
        if not isinstance(dependencies["_primary_in"], torch.Tensor):
            raise NodeProcessError(self, "primary input is not a tensor")

    def calculate(self, dependencies):
        # Apply gamma encoding
        if dependencies["_primary_in"] is None:
            return None

        return RenderNode.encode_gamma(dependencies["_primary_in"], self.gamma)
