from classes.znode import ZNode
from kazoo.client import KazooClient
from handlers.json_file import load_json_file, dict_to_json


class ZNodeTree:
    def __init__(self, zk: KazooClient, root_path='/'):
        """
        Initialize a ZNodeTree instance, which recursively builds a tree structure from a root path.

        :param zk: An instance of KazooClient connected to Zookeeper
        :param root_path: The root path of the ZNodeTree to start from
        """
        self.zk = zk
        self.root_path = f"{root_path if root_path == '/' else root_path + '/'}"


    def get_current_state(self, path=''):
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

    def update(self, json_data, env=''):

        if not env in json_data and "default_value" in json_data:
            ZNode.update(self.zk, self.root_path, json_data.get("default_value"))
            return

        if env in json_data:
            if isinstance(json_data.get(env), dict):
                self.update(json_data.get(env), env)
                return
            else:
                ZNode.update(self.zk, self.root_path ,json_data.get(env))
                return

        for path, value in json_data.items():
            path= f"{self.root_path}{path}"
            if isinstance (value, dict):
                self.update(value, env)
            else:
                ZNode.update(self.zk, path, value)

    def to_nested_dict(self, path=None):

        if path is None:
            path = self.root_path
        """
        Convert the ZNodeTree structure to a dictionary where keys are paths and values are data.
        """

        # Initialize the result dictionary
        result = {}

        children= self.zk.get_children(path)

        for child in children:
            child_path=f"{path}/{child}" if path != "/" else f"/{child}"

            data, _ = self.zk.get(child_path)
            result[child]= self.to_dict(child_path) if self.zk.get_children(child_path) else data.decode('utf-8')

        return result

    def to_flat_dict(self, path=None):

        if path is None:
            path = self.root_path

        # Initialize the result dictionary
        result = {}
        data, _ = self.zk.get(path)
        children_paths = self.zk.get_children(path)
        # Store the data in the result dictionary
        result[path] = data.decode('utf-8') if data else None
        # Recursively get data for each child path
        for child in children_paths:
            child_path = f"{path if path == '/' else path + '/'}{child}"
            result.update(self.to_flat_dict(child_path))

        return result

    def compare_states(self, current, new):
        """
        Compare two states of the ZNode tree and print created, deleted, and changed nodes.
        """
        added = {}
        deleted = {}
        changed = {}

        for key in new:
            if key not in current:
                added[key] = new[key]  # Key is new
            elif current[key] != new[key]:
                changed[key] = {'current_value': current[key], 'new': new[key]}  # Key has different value

        # Check for deleted keys
        for key in current:
            if key not in new:
                deleted[key] = current[key]  # Key is missing in new_dict

        for key in added:
            print(f"++ {key} added with value: {added[key]}")
        for key in deleted:
            print(f"-- {key} deleted")
        for key, values in changed.items():
            print(f"** {key} changed from {values['current_value']} to {values['new_value']}")

    def backup(self):
        dict_to_json(self.root_path,self.to_nested_dict(self.root_path))


