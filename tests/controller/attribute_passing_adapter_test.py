import torch
from PySide6 import QtGui

from controller.attribute_passing_adapter import _camel_to_snake
from controller.attribute_passing_adapter import attribute_dict_rename_adapter
from controller.attribute_passing_adapter import attribute_dict_camel_case_adapter
from controller.attribute_passing_adapter import (
    attribute_dict_qt_to_torch_value_adapter,
)


def test_camel_case_conversion():
    assert _camel_to_snake("variableName") == "variable_name"
    assert _camel_to_snake("variableNameTest") == "variable_name_test"
    assert _camel_to_snake("variableABCTest") == "variable_abc_test"
    assert _camel_to_snake("Test") == "test"
    assert _camel_to_snake("TestABC") == "test_abc"
    assert _camel_to_snake("TestABCDefinitely") == "test_abc_definitely"


def test_rename_adapter_basic():
    d = {"a": 1, "b": 2, "c": 3}

    ex = {"b": "x"}

    assert attribute_dict_rename_adapter(d, ex) == {"a": 1, "x": 2, "c": 3}


def test_rename_adapter_multiple():
    d = {"a": 1, "b": 2, "c": 3}

    ex = {"b": "x", "c": "y"}

    assert attribute_dict_rename_adapter(d, ex) == {"a": 1, "x": 2, "y": 3}


def test_rename_adapter_none():
    d = {"a": 1, "b": 2, "c": 3}

    assert attribute_dict_rename_adapter(d, {}) == {**d}


def test_camel_case_adapter():
    d = {"a": 1, "camelCase": 2, "c": 3}

    assert attribute_dict_camel_case_adapter(d) == {"a": 1, "camel_case": 2, "c": 3}


def test_qt_to_torch_value_adapter():
    d = {"a": 1, "b": QtGui.QColor("cyan"), "c": 3}

    res = attribute_dict_qt_to_torch_value_adapter(d)

    assert len(res) == 3
    assert "a" in res
    assert "b" in res
    assert "c" in res
    assert res["a"] == 1
    assert torch.equal(res["b"], torch.tensor([0.0, 1.0, 1.0]))
    assert res["c"] == 3
