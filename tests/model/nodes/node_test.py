import pytest
from unittest.mock import Mock

from concurrent.futures import ThreadPoolExecutor

from model.nodes.node import BaseNode


class TestStartingNodeOne(BaseNode):
    def __init__(self):
        super().__init__()
        self.test = None

    def check_requirements(self):
        return True

    def calculate(self, dependencies):
        return 1


class TestOperationNodeAddTwo(BaseNode):
    def __init__(self):
        super().__init__()
        self.test = None

    def check_requirements(self):
        return "input" in self.input_connections

    def calculate(self, dependencies):
        return dependencies["input"] + 2


class TestOperationNodeAdd(BaseNode):
    def __init__(self):
        super().__init__()
        self.test = None

    def check_requirements(self):
        return "input1" in self.input_connections and "input2" in self.input_connections

    def calculate(self, dependencies):
        return dependencies["input1"] + dependencies["input2"]


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


@pytest.mark.timeout(1)
def test_basic_multi_input_operation():
    n1 = TestStartingNodeOne()
    n2 = TestStartingNodeOne()

    n3 = TestOperationNodeAdd()

    n3.set_input_connection("input1", n1)
    n3.set_input_connection("input2", n2)

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n3.process(executor).result() == 2


@pytest.mark.timeout(1)
def test_operation_two_input_paths():
    n1 = TestStartingNodeOne()
    n2 = TestStartingNodeOne()

    n3 = TestOperationNodeAddTwo()
    n4 = TestOperationNodeAddTwo()

    n5 = TestOperationNodeAdd()

    n3.set_input_connection("input", n1)
    n4.set_input_connection("input", n2)

    n5.set_input_connection("input1", n3)
    n5.set_input_connection("input2", n4)

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n5.process(executor).result() == 6


@pytest.mark.timeout(1)
def test_basic_operation_is_cached():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n2.calculate = Mock(return_value=3)

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n2.process(executor).result() == 3
        n2.calculate.assert_called_once()

        assert n2.process(executor).result() == 3
        n2.calculate.assert_called_once()


@pytest.mark.timeout(1)
def test_basic_operation_is_dirty_when_attribute_changed():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n2.calculate = Mock(return_value=3)

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n2.process(executor).result() == 3
        n2.calculate.assert_called_once()

        n2.set_attribute("test", 1)

        assert n2.process(executor).result() == 3
        assert n2.calculate.call_count == 2


@pytest.mark.timeout(1)
def test_operation_two_input_paths_is_cached():
    n1 = TestStartingNodeOne()
    n2 = TestStartingNodeOne()

    n3 = TestOperationNodeAddTwo()
    n4 = TestOperationNodeAddTwo()

    n5 = TestOperationNodeAdd()

    n3.set_input_connection("input", n1)
    n4.set_input_connection("input", n2)

    n5.set_input_connection("input1", n3)
    n5.set_input_connection("input2", n4)

    n5.calculate = Mock(return_value=6)

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n5.process(executor).result() == 6
        n5.calculate.assert_called_once()

        assert n5.process(executor).result() == 6
        n5.calculate.assert_called_once()


@pytest.mark.timeout(1)
def test_operation_two_input_paths_is_dirty_when_attribute_changed_early():
    n1 = TestStartingNodeOne()
    n2 = TestStartingNodeOne()

    n3 = TestOperationNodeAddTwo()
    n4 = TestOperationNodeAddTwo()

    n5 = TestOperationNodeAdd()

    n3.set_input_connection("input", n1)
    n4.set_input_connection("input", n2)

    n5.set_input_connection("input1", n3)
    n5.set_input_connection("input2", n4)

    n5.calculate = Mock(return_value=6)

    with ThreadPoolExecutor(max_workers=1) as executor:
        assert n5.process(executor).result() == 6
        n5.calculate.assert_called_once()

        n1.set_attribute("test", 1)

        assert n5.process(executor).result() == 6
        assert n5.calculate.call_count == 2
