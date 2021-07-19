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

    def set_attribute(self, name, value):
        if not (hasattr(self, name) and getattr(self, name) == value):
            setattr(self, name, value)
            self._dirty = True

    def flag_dirty(self):
        for node in self.input_connections.values():
            if node.flag_dirty():
                self._dirty = True

        return self._dirty

    def calculate(self, dependencies):
        raise NotImplementedError("calculate should be implemented in subclasses")

    def _calculate(self, dependencies):
        if not self._dirty:
            return self._result

        # Wait for dependency calculation completion
        dependencies = {k: v.result() for k, v in dependencies.items()}

        self._result = self.calculate(dependencies)
        self._dirty = False

        return self._result

    def process(self, executor, check_dirty=True):
        if not self.check_required_connections():
            return executor.submit(lambda: None)

        if check_dirty:
            self.flag_dirty()

        # Queue dependent results
        dependencies = {
            k: v.process(executor, check_dirty=False)
            for k, v in self.input_connections.items()
        }

        return executor.submit(self._calculate, dependencies)
