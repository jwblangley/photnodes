import pytest
from concurrent.futures import ThreadPoolExecutor

from model.nodes.node import BaseNode


class TestStartingNodeOne(BaseNode):
    def __init__(self):
        super().__init__()

    def check_required_connections(self):
        return True

    def calculate(self, dependencies):
        return 1


class TestOperationNodeAddTwo(BaseNode):
    def __init__(self):
        super().__init__()

    def check_required_connections(self):
        return "input" in self.input_connections

    def calculate(self, dependencies):
        return dependencies["input"] + 2


@pytest.mark.timeout(1)
def test_base_node_raises_not_implemented():
    node = BaseNode()

    with ThreadPoolExecutor(max_workers=1) as executor:
        with pytest.raises(NotImplementedError):
            node.process(executor)


@pytest.mark.timeout(1)
def test_basic_operation():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n2.process(executor).result() == 3


@pytest.mark.timeout(1)
def test_no_required_input_returns_none():
    n2 = TestOperationNodeAddTwo()

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n2.process(executor).result() is None


@pytest.mark.timeout(1)
def test_removed_required_input_returns_none():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n2.remove_input_connection("input")

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n2.process(executor).result() is None
