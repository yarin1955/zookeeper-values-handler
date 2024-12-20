from kazoo.client import KazooClient
class ZNode:
    def __init__(self, path ,data=None, children=None):
        """
        Initialize a ZNode instance.

        :param path: Path of the node in Zookeeper
        :param data: Data stored in the node
        :param children: List of child ZNode instances
        """
        self.path = path
        self.data = data
        self.children = children if children is not None else []

    def __str__(self):
        return f"path: {self.path}, data: {self.data}"

    @staticmethod
    def update(zk: KazooClient,path, value):
        if zk.exists(path):
            # If the node exists, update its value
            zk.set(path, value.encode('utf-8'))
            print(f"Node {path} updated with value: {value}")
        else:
            # If the node doesn't exist, create it with the specified value
            zk.create(path, value.encode('utf-8'), makepath=True)
            print(f"Node {path} created with value: {value}")

    def __repr__(self):
        """
        String representation of the ZNode.
        """
        return f"ZNode(path={self.path}, data={self.data}, children_count={len(self.children)})"
