import view.nodes.connection


class BaseNode:
    def __init__(self):
        self.input_connections = {}
        self.output_connections = {}

        self._result = None

    def set_input_connection(self, name, input_connection):
        self.input_connections[name] = input_connection

    def set_output_connection(self, name, output_connection):
        self.output_connections[name] = output_connection

    def remove_input_connection(self, name):
        if name in self.input_connections:
            del self.input_connections[name]

    def remove_output_connection(self, name):
        if name in self.output_connections:
            del self.output_connections[name]

    def check_required_connections(self):
        raise NotImplementedError(
            "check_required_connections should be implemented in subclasses"
        )

    def calculate(self, dependencies):
        raise NotImplementedError("calculate should be implemented in subclasses")

    def _calculate(self, dependencies):
        # Wait for dependency calculation completion
        dependencies = {k: v.result() for k, v in dependencies}
        return self.calculate(dependencies)

    def process(self, executor):
        if not self.check_required_connections():
            return None

        # Queue dependent results
        dependencies = {k: v.process(executor) for k, v in self.input_connections}

        return executor.submit(self._calculate, dependencies)
