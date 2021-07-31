from model.nodes.functional.image_file_node import ImageFileNode as MImageFileNode
from model.nodes.functional.render_node import RenderNode as MRenderNode
from model.nodes.functional.solid_color_node import SolidColorNode as MSolidColorNode

from view.nodes.functional.image_file_node import ImageFileNode as VImageFileNode
from view.nodes.functional.render_node import RenderNode as VRenderNode
from view.nodes.functional.solid_color_node import SolidColorNode as VSolidColorNode

NODE_CLASS_MAP = {
    VImageFileNode: MImageFileNode,
    VRenderNode: MRenderNode,
    VSolidColorNode: MSolidColorNode,
}

NODE_CATEGORIES = {
    "Generators": [
        VSolidColorNode,
        VImageFileNode,
    ]
}
