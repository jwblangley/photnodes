import re

import torch

from PySide6 import QtGui

EXCEPTIONS = {}


def attribute_dict_rename_adapter(attr_dict, ex):
    return {ex[k] if k in ex else k: v for k, v in attr_dict.items()}


def _camel_to_snake(text):
    text = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", text).lower()


def attribute_dict_camel_case_adapter(attr_dict):
    return {_camel_to_snake(k): v for k, v in attr_dict.items()}


def _qt_to_torch_value(value):
    if isinstance(value, QtGui.QColor):
        return torch.tensor([value.red(), value.green(), value.blue()]) / 255

    return value


def attribute_dict_qt_to_torch_value_adapter(attr_dict):
    return {k: _qt_to_torch_value(v) for k, v in attr_dict.items()}


def attribute_dict_qt_to_torch_adapter(attr_dict):
    attr_dict = attribute_dict_rename_adapter(attr_dict, EXCEPTIONS)
    attr_dict = attribute_dict_camel_case_adapter(attr_dict)
    attr_dict = attribute_dict_qt_to_torch_value_adapter(attr_dict)
    return attr_dict
