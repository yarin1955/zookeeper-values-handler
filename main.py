import argparse
from classes.znodeTree import ZNodeTree
from kazoo.client import KazooClient
from handlers.json_file import load_json_file, flatten_json

def main(args):
    zk = KazooClient(hosts='127.0.0.1:2181')
    zk.start()

    # Create a ZNodeTree from the root
    ztree = ZNodeTree(zk, root_path=args.znode)

    if args.update:
        json_data= load_json_file(args.pathfile)
        ztree.update(json_data, args.env)
        ztree.compare_states(ztree.to_flat_dict(args.znode), flatten_json(json_data))
    if args.backup:
        ztree.backup()

    zk.stop()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Update or process paths")
#
# # Add the update flag (store_true means it acts like a switch, no argument required)
    parser.add_argument('--update', action='store_true', help="Trigger the update process")

    parser.add_argument('--backup', action='store_true', help="Trigger the update process")

    parser.add_argument('--env', type=str, required=True, help='Environment variable string')
    parser.add_argument('--pathfile', type=str, required=True, help='Location of the path file')
    parser.add_argument('--znode', type=str, required=True, help='ZNode string')

    args = parser.parse_args()

    main(args)
