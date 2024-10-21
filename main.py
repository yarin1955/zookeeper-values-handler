import argparse
from classes.znodeTree import ZNodeTree
from kazoo.client import KazooClient

if __name__ == "__main__":
    zk = KazooClient(hosts='127.0.0.1:2181')
    zk.start()

    # Create a ZNodeTree from the root
    ztree = ZNodeTree(zk, root_path='/')

    # Display the structure of the ZNodeTree
    # ztree.print()

    ztree.update(json_str)

    zk.stop()


# def update_function():
#     print("Performing update...")
#
# def process_path(path):
#     print(f"Processing path: {path}")
#
# # Create argument parser
# parser = argparse.ArgumentParser(description="Update or process paths")
#
# # Add the update flag (store_true means it acts like a switch, no argument required)
# parser.add_argument('--update', action='store_true', help="Trigger the update process")
#
# parser.add_argument('--restore', action='store_true', help="Trigger the update process")
#
# parser.add_argument('--backup', action='store_true', help="Trigger the update process")
#
#
# parser.add_argument('zoo_servers', action='store_true', help="Trigger the update process")
# # Add a positional argument for path (optional, only required if --update is not present)
# parser.add_argument('path', nargs='?', help="The path of znode")
#
# # Parse the arguments
# args = parser.parse_args()
#
# # Logic based on the presence of --update
# if args.backup:
#     update_function()
#
# if args.update:
#     main()  # Call the update function
#
# if args.restore:
#     update_function()
# elif args.path:
#     process_path(args.path)  # Process the provided path
# else:
#     print("No update flag or path provided. Please specify a path or use --update.")
