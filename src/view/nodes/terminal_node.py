from view.nodes.header import Header
from view.nodes.node import BaseNode
from view.nodes.socket import Socket


class TerminalNode(BaseNode):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)

        self.header = Header(self, title)
        self.header.setParentItem(self)

        self.primaryInSocket = Socket("_primaryIn", "", True, maxConnections=1)
        self.primaryInSocket.setParentItem(self)
        self.primaryInSocket.node = self
        self.sockets["_primaryIn"] = self.primaryInSocket

        self.updateSize()
