import argparse

# Change to parser and de-couple adding arguments to application specific subparsers.
class ArgumentReader:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="dt", description="An efficient structured data converter")
        self.subparsers = self.parser.add_subparsers(dest="application", help="Various commands")
        self.args = None

    def get_subparser(self):
        return self.subparsers

    def get_args(self):
        if self.args is None:
            self.args = self.parser.parse_args()

        return self.args

    def get_application(self):
        if self.args is None:
            self.args = self.parser.parse_args()

        return self.args.application