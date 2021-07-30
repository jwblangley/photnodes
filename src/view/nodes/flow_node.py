from view.nodes.header import Header
from view.nodes.node import BaseNode
from view.nodes.socket import Socket


class FlowNode(BaseNode):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)

        self.header = Header(self, title)
        self.header.setParentItem(self)

        self.primaryInSocket = Socket("_primaryIn", "", True, maxConnections=1)
        self.primaryInSocket.setParentItem(self)
        self.primaryInSocket.node = self
        self.sockets["_primaryIn"] = self.primaryInSocket

        self.primaryOutSocket = Socket("_primaryOut", "", False)
        self.primaryOutSocket.setParentItem(self)
        self.primaryOutSocket.node = self
        self.sockets["_primaryOut"] = self.primaryOutSocket

        self.updateSize()
