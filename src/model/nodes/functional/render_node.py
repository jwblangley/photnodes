from model.nodes.node import BaseNode


class _GammaNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.gamma = None

    def check_requirements(self):
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

    def __setattr__(self, name, value):
        if name == "gamma" and value is not None:
            self._gamma_node.set_attribute("gamma", value)

        return super().__setattr__(name, value)

    def check_requirements(self):
        return (
            isinstance(self.gamma, float)
            and self.gamma > 0
            and "_primary_in" in self.input_connections
        )

    def calculate(self, dependencies):
        # Apply gamma encoding
        return RenderNode.encode_gamma(dependencies["_primary_in"], self.gamma)
