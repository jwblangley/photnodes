import pytest
from concurrent.futures import ThreadPoolExecutor

from model.nodes.node import BaseNode


@pytest.mark.timeout(1)
def test_base_node_raises_not_implemented():
    node = BaseNode()

    with ThreadPoolExecutor(max_workers=1) as executor:
        with pytest.raises(NotImplementedError):
            node.process(executor)
