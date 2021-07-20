from controller.node_map import NODE_CLASS_MAP
from view.nodes.functional.solid_color_node import SolidColorNode


class Controller:
    def __init__(self, window):
        self.window = window

        self.view_model_node_map = {}

        self.new_node(SolidColorNode)

    def new_node(self, vnode_class):
        print(vnode_class)
        mnode_class = NODE_CLASS_MAP[vnode_class]
        print(mnode_class)

        vnode = vnode_class()
        mnode = mnode_class()

        self.view_model_node_map[vnode] = mnode

        self.window.nodeCanvas.addNode(vnode)
