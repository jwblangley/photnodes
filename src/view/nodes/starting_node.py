from view.nodes.header import Header
from view.nodes.node import Node
from view.nodes.socket import Socket


class StartingNode(Node):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.header = Header(self, "Input file")
        self.header.setParentItem(self)

        self.primary_out_socket = Socket("_primary_out", "", False)
        self.primary_out_socket.setParentItem(self)
        self.primary_out_socket.node = self
        self.sockets["_primary_out"] = self.primary_out_socket

        xOffset = self.margin / 2
        self.primary_out_socket.setPos(self.boundingRect().right() + xOffset, 0)
        self.updateSize()
