from classes.znode import ZNode
from kazoo.client import KazooClient
from handlers.json_file import load_json_file
from handlers.yaml import json_str


class ZNodeTree:
    def __init__(self, zk: KazooClient, root_path='/'):
        """
        Initialize a ZNodeTree instance, which recursively builds a tree structure from a root path.

        :param zk: An instance of KazooClient connected to Zookeeper
        :param root_path: The root path of the ZNodeTree to start from
        """
        self.zk = zk
        self.root_path = root_path


    def get_current_state(self, path=self.root_path):
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
        children = [self.get_current_state(f"{path if path == '/' else path + '/'}{child}") for child in children_paths]

        # Create and return the ZNode object
        return ZNode(path=path, data=data.decode("utf-8") if data else None, children=children)

    # def print(self, node=None, level=0):
    #     """
    #     Print the ZNodeTree structure starting from the root node or a specified node.
    #     """
    #     if node is None:
    #         node = self.root
    #
    #     print(f"{node.path} (data: {node.data})")
    #     for child in node.children:
    #         self.print(child, level + 1)

    def update(self, json_data, parent_znode='', env=''):

        parent_znode=f"{parent_znode if parent_znode == '/' else parent_znode + '/'}"

        if not env in json_data and "default_value" in json_data:
            ZNode.update(self.zk, parent_znode, json_data.get("default_value"))
            return

        if env in json_data:
            if isinstance(json_data.get(env), dict):
                self.update(json_data.get(env), parent_znode, env)
                return
            else:
                ZNode.update(self.zk, parent_znode, json_data.get(env))
                return

        for path, value in json_data.items():
            path= f"{parent_znode}{path}"
            if isinstance (value, dict):
                self.update(value, path, env)
            else:
                ZNode.update(self.zk, path, value)

    def to_dict(self, path=self.root_path):
        """
        Convert the ZNodeTree structure to a dictionary where keys are paths and values are data.
        """

        # Initialize the result dictionary
        result = {}

        data, _ = self.zk.get(path)

        children_paths = self.zk.get_children(path)

        # Store the data in the result dictionary
        result[path] = data.decode('utf-8') if data else None

        # Recursively get data for each child path
        for child in children_paths:
            child_path = f"{path if path == '/' else path + '/'}{child}"
            result.update(self.to_dict(child_path))

        return result

    def compare_states(self, old, new):
        """
        Compare two states of the ZNode tree and print created, deleted, and changed nodes.
        """
        created = {}
        deleted = {}
        changed = {}


    # def iterate_nested_json_for_loop(json_obj, parent_key=''):
    #     for key, value in json_obj.items():
    #         new_key = f"{parent_key}/{key}" if parent_key else f"/{key}"
    #         if isinstance(value, dict):
    #             iterate_nested_json_for_loop(value, new_key)
    #         else:
    #             print(f"{new_key}: {value}")

    # def update(self):
    #     def a="44";

    def backup(self):
        return

