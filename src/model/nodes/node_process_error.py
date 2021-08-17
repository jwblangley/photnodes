class NodeProcessError(RuntimeError):
    """
    Raised when node processing fails
    """
    def __init__(self, message):
        super().__init__(message)
