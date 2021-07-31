import torch
import numpy as np

from PySide6 import QtGui
from PySide6 import QtCore


def QImage_to_torch(qimg):
    """
    Convert RGB QImage to CxHxW torch array
    """
    qimg = qimg.convertToFormat(QtGui.QImage.Format.Format_RGB32)
    width = qimg.width()
    height = qimg.height()

    ptr = qimg.bits()
    np_img = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    torch_img = torch.Tensor(np_img)
    torch_img = torch_img.permute(2, 0, 1)
    torch_img = torch_img[:-1, :, :]
    # Flip channel order to match expected
    torch_img = torch.flip(torch_img, (0,))
    torch_img /= 255
    return torch_img


def torch_to_QImage(torch_image):
    """
    Convert CxHxW torch array [0..1] to RGB QImage
    N.B: data buffer must remain in scope for lifetime of QImage
    """
    torch_image = torch_image.clone()
    torch_image *= 255
    torch_image.clamp_(0, 255)
    torch_image = torch_image.permute(1, 2, 0)

    img = torch_image.cpu().numpy()
    # Flip channel order to match expected
    np.flip(img, axis=2)

    rgba = np.full((img.shape[0], img.shape[1], 4), 255, dtype=np.uint8)
    rgba[:, :, :-1] = img

    height, width, channels = rgba.shape

    data = QtCore.QByteArray(rgba.data.tobytes())

    qImg = QtGui.QImage(
        data,
        width,
        height,
        QtGui.QImage.Format_RGB32,
    )

    return qImg, data
