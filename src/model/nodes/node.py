class BaseNode:
    def __init__(self):
        self.input_connections = {}

        self._dirty = True
        self._result = None

    def set_input_connection(self, name, input_connection):
        self.input_connections[name] = input_connection

    def remove_input_connection(self, name):
        if name in self.input_connections:
            del self.input_connections[name]

    def check_required_connections(self):
        raise NotImplementedError(
            "check_required_connections should be implemented in subclasses"
        )

    def is_dirty(self):
        if self._dirty:
            return True

        for node in self.input_connections.values():
            if node.is_dirty():
                return True

        return False

    def calculate(self, dependencies):
        raise NotImplementedError("calculate should be implemented in subclasses")

    def _calculate(self, dependencies):
        if not self.is_dirty():
            return self._result

        # Wait for dependency calculation completion
        dependencies = {k: v.result() for k, v in dependencies.items()}

        self._result = self.calculate(dependencies)
        self._dirty = False

        return self._result

    def process(self, executor):
        if not self.check_required_connections():
            return executor.submit(lambda: None)

        # Queue dependent results
        dependencies = {
            k: v.process(executor) for k, v in self.input_connections.items()
        }

        return executor.submit(self._calculate, dependencies)
