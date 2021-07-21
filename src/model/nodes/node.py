class BaseNode:
    def __init__(self):
        self.input_connections = {}

        self.output_connections = []

        self._dirty = True
        self._result = None

    def destroy(self):
        for listener in self.output_connections:
            listener.input_connections = {
                k: v for k, v in listener.input_connections.items() if v != self
            }

    def set_input_connection(self, name, input_connection):
        self.input_connections[name] = input_connection
        input_connection.output_connections.append(self)

    def remove_input_connection(self, name):
        if name in self.input_connections:
            input_connection = self.input_connections[name]
            input_connection.output_connections = list(
                filter(lambda c: c != self, input_connection.output_connections)
            )
            del self.input_connections[name]

    def check_requirements(self):
        raise NotImplementedError(
            "check_requirements should be implemented in subclasses"
        )

    def set_attribute(self, name, value):
        if not hasattr(self, name):
            raise AttributeError(f"Node does not have attribute: {name}")

        setattr(self, name, value)
        self.flag_dirty()

    def flag_dirty(self):
        self._dirty = True

        for node in self.output_connections:
            node.flag_dirty()

    def calculate(self, dependencies):
        raise NotImplementedError("calculate should be implemented in subclasses")

    def _calculate(self, dependencies):
        if not self._dirty:
            return self._result

        self._result = self.calculate(dependencies)
        self._dirty = False

        return self._result

    def process(self, check_dirty=True):
        if not self.check_requirements():
            return None

        if check_dirty:
            self._dirty

        # Queue dependent results
        dependencies = {
            k: v.process(check_dirty=False) for k, v in self.input_connections.items()
        }

        return self._calculate(dependencies)
