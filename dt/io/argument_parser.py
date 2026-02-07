import argparse

# Change to parser and de-couple adding arguments to application specific subparsers.
class ArgumentReader:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="dt", description="An efficient structured data converter")
        self.parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
        self.subparsers = self.parser.add_subparsers(dest="application", help="Various commands")
        self.args = None

    def get_subparser(self):
        return self.subparsers

    def get_args(self):
        if self.args is None:
            self.args = self.parser.parse_args()

        return self.args
    
    def get_arg(self, arg_name: str):
        if self.args is None:
            self.args = self.parser.parse_args()

        return getattr(self.args, arg_name)

    def get_application(self):
        return self.get_arg("application")

    def get_verbose(self):
        return self.get_arg("verbose")