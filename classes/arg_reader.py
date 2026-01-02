import argparse, os, re

class ArgumentReader:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="dt", description="An efficient structured data converter")
        subparsers = parser.add_subparsers(dest="application", help="Various commands")

        # Setup transform application.
        transform_parser = subparsers.add_parser("transform", description="Application performs data transformations based on the specified configuration")
        transform_parser.add_argument("-c", "--config", required=True, type=str, help="path to the configuration file")
        transform_parser.add_argument("paths", nargs="+", type=str, help="the path to the bank statement file")
        transform_parser.add_argument("-a", "--append", action="store_true", help="append to the output file instead of overwriting")
        transform_parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
        transform_parser.add_argument("-o", "--output", type=str, default="output.csv", help="the path to the output file (default: output.csv)")

        # Setup config application.
        config_parser = subparsers.add_parser("config")
        config_modes = config_parser.add_subparsers(dest="mode", help="Config applications")

        config_modes_add = config_modes.add_parser("add")
        config_modes_add.add_argument('file', type=str, help="Location of the config file")

        config_modes.add_parser("list")

        config_modes_delete = config_modes.add_parser("delete")
        config_modes_delete.add_argument('name', type=str, help="Name of the configuration to be deleted")

        self.args = parser.parse_args()

    def get_application(self):
        return self.args.application