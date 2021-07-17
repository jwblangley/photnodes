from view.nodes.header import Header
from view.nodes.node import BaseNode
from view.nodes.socket import Socket


class TerminalNode(BaseNode):
    def __init__(self, title, **kwargs):
        super().__init__(title, **kwargs)

        self.header = Header(self, title)
        self.header.setParentItem(self)

        self.primary_out_socket = Socket("_primary_in", "", True, maxConnections=1)
        self.primary_out_socket.setParentItem(self)
        self.primary_out_socket.node = self
        self.sockets["_primary_in"] = self.primary_out_socket

        self.updateSize()
