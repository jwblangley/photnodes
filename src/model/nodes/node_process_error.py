class NodeProcessError(RuntimeError):
    """
    Raised when node processing fails
    """
    def __init__(self, node, message):
        super().__init__(f"{type(node).__name__}: {message}")

        self.node = node
