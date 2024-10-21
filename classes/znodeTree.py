import re
from classes.znode import ZNode
from kazoo.client import KazooClient
class ZNodeTree:
    def __init__(self, zk: KazooClient, root_path='/'):
        """
        Initialize a ZNodeTree instance, which recursively builds a tree structure from a root path.

        :param zk: An instance of KazooClient connected to Zookeeper
        :param root_path: The root path of the ZNodeTree to start from
        """
        self.zk = zk
        self.root = self.set(root_path)


    def set(self, path):
        """
        Recursively build the ZNodeTree from a given path.

        :param path: Zookeeper node path
        :return: ZNode instance with its children recursively populated
        """
        # Fetch node data

        data, _ = self.zk.get(path)

        # Fetch children of the current node
        children_paths = self.zk.get_children(path)

        # Recursively create ZNode objects for each child
        children = [self.set(f"{path if path == '/' else path + '/'}{child}") for child in children_paths]

        # Create and return the ZNode object
        return ZNode(path=path, data=data.decode("utf-8") if data else None, children=children)

    def print(self, node=None, level=0):
        """
        Print the ZNodeTree structure starting from the root node or a specified node.
        """
        if node is None:
            node = self.root

        print(f"{node.path} (data: {node.data})")
        for child in node.children:
            self.print(child, level + 1)

    def update(self, json_data, parent_key=''):
        for key, value in json_data.items():
            new_key = f"{parent_key}/{key}" if parent_key else f"/{key}"
            if isinstance(value, dict):
                self.update(value, new_key)
            else:
                # print(f"{new_key}: {value}")
                if self.zk.exists(new_key):
                    # If the node exists, update its value
                    self.zk.set(new_key, value.encode('utf-8'))
                    print(f"Node {new_key} updated with value: {value}")
                else:
                    # If the node doesn't exist, create it with the specified value
                    self.zk.create(new_key, value.encode('utf-8'), makepath=True)
                    print(f"Node {new_key} created with value: {value}")


    # def iterate_nested_json_for_loop(json_obj, parent_key=''):
    #     for key, value in json_obj.items():
    #         new_key = f"{parent_key}/{key}" if parent_key else f"/{key}"
    #         if isinstance(value, dict):
    #             iterate_nested_json_for_loop(value, new_key)
    #         else:
    #             print(f"{new_key}: {value}")

    # def update(self):
    #     def a="44";

