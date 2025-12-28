import argparse, os, re

class ArgumentReader:
    def __init__(self):
        parser = argparse.ArgumentParser(prog="dt", description="An efficient structured data converter")

        # Positional arguments.
        parser.add_argument("paths", nargs="+", type=str, help="the path to the bank statement file")

        # Required arguments.
        parser.add_argument("-c", "--config-file", required=True, type=str, help="path to the configuration file")

        # Optional arguments.
        parser.add_argument("-a", "--append", action="store_true", help="append to the output file instead of overwriting")
        parser.add_argument("-v", "--verbose", action="store_true", help="enable verbose output")
        parser.add_argument("-o", "--output", type=str, default="output.csv", help="the path to the output file (default: output.csv)")

        self.args = parser.parse_args()
        
    def get_paths(self) -> list[str]:
        """Get a list of valid file paths from the provided arguments."""
        file_paths = []

        for path in self.args.paths:
            if os.path.exists(path) is False:
                raise FileNotFoundError(f"File not found: {path}")
            elif os.path.isdir(path) is True:
                for file in os.listdir(path):
                    full_path = os.path.join(path, file)
                    if os.path.isfile(full_path) is True and re.match(r".*\.(csv|CSV)$", file):
                        file_paths.append(full_path)
            elif os.path.isfile(path) is True:
                file_paths.append(path)
            else:
                raise ValueError(f"Path is not a file or directory: {path}")

        return file_paths
    
    def get_verbose(self) -> bool:
        """Get the verbose flag as a boolean."""
        return self.args.verbose
    
    def get_config(self) -> str:
        """Get the configuration file path."""
        return self.args.config_file
    
    def get_append(self) -> bool:
        """Get the append flag as a boolean."""
        return self.args.append
    
    def get_output(self) -> str:
        """Get the output file path."""
        return self.args.output
    
    def __str__(self):
        str = "ArgumentReader:\n"

        str += f"(verbose, {self.get_verbose()})\n"
        str += f"(append, {self.get_append()})\n"
        str += f"(output, {self.get_output()})\n"

        for index, path in enumerate(self.get_paths()):
            str += f"({index}, {os.path.basename(path)}, {os.path.getsize(path)} bytes)\n"

        return str
    