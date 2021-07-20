from model.nodes.functional.render_node import RenderNode as MRenderNode
from model.nodes.functional.solid_color_node import SolidColorNode as MSolidColorNode

from view.nodes.functional.render_node import RenderNode as VRenderNode
from view.nodes.functional.solid_color_node import SolidColorNode as VSolidColorNode

NODE_CLASS_MAP = {
    VRenderNode: MRenderNode,
    VSolidColorNode: MSolidColorNode,
}
