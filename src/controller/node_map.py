from model.nodes.functional.solid_color_node import SolidColorNode as MSolidColorNode

from view.nodes.functional.solid_color_node import SolidColorNode as VSolidColorNode

NODE_CLASS_MAP = {
    VSolidColorNode: MSolidColorNode,
}
