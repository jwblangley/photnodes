from PySide6 import QtGui
from PySide6 import QtCore


def getTextSize(text, painter=None):
    if not painter:
        metrics = QtGui.QFontMetrics(QtGui.QFont())
    else:
        metrics = painter.fontMetrics()
    size = metrics.size(QtCore.Qt.TextSingleLine, text)
    return size
