import numpy as np
import torch

from model.image_io.rawpy.rawpy_io import (
    load_neutral_image_16_bit as rawpy_load_neutral_image_16_bit,
)

MAX_16_BIT = 2 ** 16 - 1


def _rawpy_to_torch_adapter(path):
    np_img = rawpy_load_neutral_image_16_bit(path).astype(np.int32)
    img = torch.from_numpy(np_img)
    img = img.permute(2, 0, 1)
    img = img / MAX_16_BIT
    return img


def load_neutral_image(path):
    return _rawpy_to_torch_adapter(path)
