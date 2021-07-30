from controller.image_adapter import torch_to_QImage
from controller.node_map import NODE_CLASS_MAP
from controller.attribute_passing_adapter import attribute_dict_qt_to_torch_adapter

from view.nodes.functional.render_node import RenderNode


class Controller:
    def __init__(self, window):
        self.window = window

        self.view_model_node_map = {}

        self.left_selected_node = None
        self.right_selected_node = None

        self.render_node = None

    def initialise(self):
        self.render_node, _ = self.new_node(RenderNode)
        self.set_right_selected_node(self.render_node)

        self.update_image_canvases()

    def new_node(self, vnode_class):
        mnode_class = NODE_CLASS_MAP[vnode_class]

        vnode = vnode_class()
        mnode = mnode_class()

        self.view_model_node_map[vnode] = mnode
        vnode.passAllAttributes()

        # All non-render nodes have access to the render node's gamma
        if vnode_class != RenderNode:
            m_render_node = self.view_model_node_map[self.render_node]
            mnode.set_input_connection("gamma", m_render_node._gamma_node)

        self.window.nodeCanvas.addNode(vnode)
        self.update_image_canvases()

        return vnode, mnode

    def remove_node(self, vnode):
        mnode = self.view_model_node_map[vnode]

        vnode.destroy()
        mnode.destroy()

        self.update_image_canvases()

    def pass_attribute(self, vnode, name, value):
        attr_dict = {name: value}
        attr_dict = attribute_dict_qt_to_torch_adapter(attr_dict)

        mnode = self.view_model_node_map[vnode]
        for attr in attr_dict:
            mnode.set_attribute(attr, attr_dict[attr])

        self.update_image_canvases()

    def _connection_info(self, vconnection):
        vsocket_source = vconnection.sourceSocket
        vsocket_target = vconnection.targetSocket

        if vsocket_source.isInput:
            temp = vsocket_source
            vsocket_source = vsocket_target
            vsocket_target = temp

        vnode_source = vsocket_source.node
        vnode_target = vsocket_target.node

        mnode_source = self.view_model_node_map[vnode_source]
        mnode_target = self.view_model_node_map[vnode_target]

        connection_name = vsocket_target.name
        connection_name = next(
            iter(attribute_dict_qt_to_torch_adapter({connection_name: None}).keys())
        )

        return connection_name, mnode_source, mnode_target

    def pass_new_connection(self, vconnection):
        (
            connection_name,
            mnode_source,
            mnode_target,
        ) = self._connection_info(vconnection)

        mnode_target.set_input_connection(connection_name, mnode_source)
        self.update_image_canvases()

    def pass_remove_connection(self, vconnection):
        (
            connection_name,
            mnode_source,
            mnode_target,
        ) = self._connection_info(vconnection)

        mnode_target.remove_input_connection(connection_name)
        self.update_image_canvases()

    def update_image_canvases(self):
        left_img, left_img_buffer = self.process_node(self.left_selected_node)
        right_img, right_img_buffer = self.process_node(self.right_selected_node)

        self.window.leftImageCanvas.paintImage(left_img, left_img_buffer)
        self.window.rightImageCanvas.paintImage(right_img, right_img_buffer)

    def process_node(self, vnode, encode_gamma=True):
        if vnode is None:
            return None, None

        mnode = self.view_model_node_map[vnode]
        img = mnode.process()

        if img is None:
            return None, None

        if encode_gamma and not isinstance(vnode, RenderNode):
            img = self.encode_gamma(img)

        return torch_to_QImage(img)

    def set_left_selected_node(self, vnode):
        if self.left_selected_node is not None:
            self.left_selected_node.header.displayedLeft = False
            self.left_selected_node.header.update()

        self.left_selected_node = vnode
        self.left_selected_node.header.displayedLeft = True
        self.left_selected_node.header.update()
        self.update_image_canvases()

    def set_right_selected_node(self, vnode):
        if self.right_selected_node is not None:
            self.right_selected_node.header.displayedRight = False
            self.right_selected_node.header.update()

        self.right_selected_node = vnode
        self.right_selected_node.header.displayedRight = True
        self.right_selected_node.header.update()
        self.update_image_canvases()

    def encode_gamma(self, img):
        return img.pow(1 / self.render_node.gamma)
