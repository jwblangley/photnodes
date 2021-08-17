import pytest
from unittest.mock import Mock

import torch

from model.nodes.node import BaseNode

from model.nodes.functional.render_node import RenderNode
from model.nodes.node_process_error import NodeProcessError


class TestStartingNodeOne(BaseNode):
    def __init__(self):
        super().__init__()
        self.test = None

    def check_requirements(self, dependencies):
        pass

    def calculate(self, dependencies):
        return 1


class TestOperationNodeAddTwo(BaseNode):
    def __init__(self):
        super().__init__()
        self.test = None

    def check_requirements(self, dependencies):
        if "input" not in dependencies:
            raise NodeProcessError("No input")

    def calculate(self, dependencies):
        return dependencies["input"] + 2


class TestOperationNodeAdd(BaseNode):
    def __init__(self):
        super().__init__()
        self.test = None

    def check_requirements(self, dependencies):
        if "input1" not in dependencies:
            raise NodeProcessError("No input1")
        if "input2" not in dependencies:
            raise NodeProcessError("No input2")

    def calculate(self, dependencies):
        return dependencies["input1"] + dependencies["input2"]


def test_base_node_raises_not_implemented():
    node = BaseNode()

    with pytest.raises(NotImplementedError):
        node.process()


def test_basic_operation():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)

    assert n2.process() == 3


def test_no_required_input_raises_processing_error():
    n2 = TestOperationNodeAddTwo()

    with pytest.raises(NodeProcessError):
        n2.process()


def test_removed_required_input_raises_processing_error():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n2.remove_input_connection("input")

    with pytest.raises(NodeProcessError):
        n2.process()


def test_basic_multi_input_operation():
    n1 = TestStartingNodeOne()
    n2 = TestStartingNodeOne()

    n3 = TestOperationNodeAdd()

    n3.set_input_connection("input1", n1)
    n3.set_input_connection("input2", n2)

    assert n3.process() == 2


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

    assert n5.process() == 6


def test_basic_operation_is_cached():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n2.calculate = Mock(return_value=3)

    assert n2.process() == 3
    n2.calculate.assert_called_once()

    assert n2.process() == 3
    n2.calculate.assert_called_once()


def test_basic_operation_is_dirty_when_attribute_changed():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n2.calculate = Mock(return_value=3)

    assert n2.process() == 3
    n2.calculate.assert_called_once()

    n2.set_attribute("test", 1)

    assert n2.process() == 3
    assert n2.calculate.call_count == 2


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

    assert n5.process() == 6
    n5.calculate.assert_called_once()

    assert n5.process() == 6
    n5.calculate.assert_called_once()


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

    assert n5.process() == 6
    n5.calculate.assert_called_once()

    n1.set_attribute("test", 1)

    assert n5.process() == 6
    assert n5.calculate.call_count == 2


def test_destroy_removes_connections():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()
    n3 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n3.set_input_connection("input", n2)

    n2.destroy()

    assert "input" not in n3.input_connections


def test_destroy_does_not_side_effect():
    n1 = TestStartingNodeOne()
    n2 = TestOperationNodeAddTwo()
    n3 = TestOperationNodeAddTwo()
    n4 = TestOperationNodeAddTwo()

    n2.set_input_connection("input", n1)
    n3.set_input_connection("input", n2)
    n4.set_input_connection("input", n3)

    n3.destroy()

    assert "input" in n2.input_connections


def test_gamma_change_in_render_node_makes_previous_dirty():
    n1 = TestStartingNodeOne()

    r1 = RenderNode()
    r1.set_attribute("gamma", 1.0)

    n1.set_input_connection("gamma", r1._gamma_node)

    r1.set_input_connection("_primary_in", n1)

    n1.calculate = Mock(return_value=torch.tensor([1.0]))

    assert r1.process() == 1
    n1.calculate.assert_called_once()

    r1.set_attribute("gamma", 2.0)

    assert r1.process() == 1
    assert n1.calculate.call_count == 2
