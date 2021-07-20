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

    def _connection_participants(self, vconnection):
        vsocket_source = vconnection.sourceSocket
        vsocket_target = vconnection.targetSocket

        if not vsocket_source.isInput:
            temp = vsocket_source
            vsocket_source = vsocket_target
            vsocket_target = temp

        vnode_source = vsocket_source.node
        vnode_target = vsocket_target.node

        mnode_source = self.view_model_node_map[vnode_source]
        mnode_target = self.view_model_node_map[vnode_target]

        return vsocket_source, vnode_source, vnode_target, mnode_source, mnode_target

    def create_connection(self, vconnection):
        (
            vsocket_source,
            vnode_source,
            vnode_target,
            mnode_source,
            mnode_target,
        ) = self._connection_participants(vconnection)

        connection_name = vsocket_source.name
        connection_name = attribute_dict_qt_to_torch_adapter(
            {connection_name: None}
        ).keys()[0]

        mnode_target.set_input_connection(connection_name, mnode_source)
