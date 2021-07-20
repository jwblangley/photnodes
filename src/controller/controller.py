from controller.node_map import NODE_CLASS_MAP
from controller.attribute_passing_adapter import attribute_dict_qt_to_torch_adapter


class Controller:
    def __init__(self, window):
        self.window = window

        self.view_model_node_map = {}

    def new_node(self, vnode_class):
        print(vnode_class)
        mnode_class = NODE_CLASS_MAP[vnode_class]
        print(mnode_class)

        vnode = vnode_class()
        mnode = mnode_class()

        self.view_model_node_map[vnode] = mnode

        self.window.nodeCanvas.addNode(vnode)

    def pass_attribute(self, vnode, name, value):
        attr_dict = {name: value}
        attr_dict = attribute_dict_qt_to_torch_adapter(attr_dict)

        mnode = self.view_model_node_map[vnode]
        for attr in attr_dict:
            mnode.set_attribute(attr, attr_dict[attr])
