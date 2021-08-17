import torchvision.transforms.functional as ttf

from controller.image_adapter import torch_to_QImage
from controller.node_map import NODE_CLASS_MAP
from controller.attribute_passing_adapter import attribute_dict_qt_to_torch_adapter
from model.nodes.node_process_error import NodeProcessError

from view.nodes.functional.render_node import RenderNode

from model.nodes.functional.render_node import RenderNode as MRenderNode

MAX_PREVIEW_SIZE = 1024


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

    def get_vnode_from_mnode(self, mnode):
        """
        Should be avoided when possible in favour of dictionary lookup with view_model_node_map
        """
        for k, v in self.view_model_node_map.items():
            if v == mnode:
                return k

        return None

    def report_status(self, status, status_source=None):
        self.window.showStatus(status, status_source)

    def clear_report_status(self):
        self.window.clearStatus()

    def new_node(self, vnode_class):
        mnode_class = NODE_CLASS_MAP[vnode_class]

        vnode = vnode_class()
        mnode = mnode_class()

        self.view_model_node_map[vnode] = mnode
        vnode.passAllAttributes()

        # Required nodes have access to the render node's gamma
        if mnode_class.REQUIRES_GAMMA_CONNECTION:
            m_render_node = self.view_model_node_map[self.render_node]
            mnode.set_input_connection("gamma", m_render_node._gamma_node)

        self.window.nodeCanvas.addNode(vnode)
        self.window.nodeCanvas.selectItem(vnode)
        self.update_image_canvases()

        return vnode, mnode

    def remove_node(self, vnode):
        mnode = self.view_model_node_map[vnode]

        vnode.destroy()
        mnode.destroy()

        if self.left_selected_node is vnode:
            self.left_selected_node = None

        if self.right_selected_node is vnode:
            self.right_selected_node = None

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
        self.clear_report_status()

        try:
            left_img, left_img_buffer = self.process_node(
                self.left_selected_node, max_size=MAX_PREVIEW_SIZE
            )
        except NodeProcessError as npe:
            self.report_status(
                str(npe), status_source=self.get_vnode_from_mnode(npe.node)
            )
            left_img = None
            left_img_buffer = None

        try:
            right_img, right_img_buffer = self.process_node(
                self.right_selected_node, max_size=MAX_PREVIEW_SIZE
            )
        except NodeProcessError as npe:
            self.report_status(
                str(npe), status_source=self.get_vnode_from_mnode(npe.node)
            )
            right_img = None
            right_img_buffer = None

        self.window.leftImageCanvas.paintImage(left_img, left_img_buffer)
        self.window.rightImageCanvas.paintImage(right_img, right_img_buffer)

    def process_node(self, vnode, encode_gamma=True, max_size=None):
        if vnode is None:
            return None, None

        mnode = self.view_model_node_map[vnode]
        img = mnode.process()

        if max_size is not None:
            if max(img.shape) >= max_size:
                img = ttf.resize(img, max_size // 2, max_size=max_size)

        if encode_gamma and not isinstance(vnode, RenderNode):
            img = MRenderNode.encode_gamma(img, self.render_node.gamma)

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
