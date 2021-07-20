from model.nodes.node import BaseNode


class RenderNode(BaseNode):
    def __init__(self):
        super().__init__()
        self.gamma = None

    def check_requirements(self):
        return (
            isinstance(self.gamma, float)
            and self.gamma > 0
            and "_primary_in" in self.input_connections
        )

    def calculate(self, dependencies):
        return dependencies["_primary_in"]
