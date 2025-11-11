#!csvt/bin/python3
from classes.arg_reader import ArgumentReader
from classes.reader import ReaderFactory
from classes.transform import Transformer
from classes.writer import Writer
from classes.config import Config

def main():
    try:
        arg_reader = ArgumentReader()
        config = Config(arg_reader.get_config())

        try:
            readers = ReaderFactory.create_readers(
                arg_reader.get_paths(),
                headers=config.headers(),
                verbose=arg_reader.get_verbose()
            )

            transformer = Transformer(arg_reader.get_verbose())
            transformer.set_transforms(config.transforms())

            writer = Writer(
                arg_reader.get_output(),
                verbose=arg_reader.get_verbose(),
                append=arg_reader.get_append()
            )

            for reader in readers:
                try: 
                    df = reader.read()
                except Exception as e:
                    print(f"Error reading file {reader.file_path}: {e}")
                    return
                
                try: 
                    df = transformer.transform(df)
                except Exception as e:
                    print(f"Error transforming data from file {reader.file_path}: {e}")
                    return
                    
                try:
                    writer.add_entry(df)
                except Exception as e:
                    print(f"Error adding data from file {reader.file_path} to writer: {e}")
                    return
                
            try:
                writer.write()
            except Exception as e:
                print(f"Error writing output file {writer.file_path}: {e}")
                return
            
        except Exception as e:
            print(f"Error creating readers: {e}")
            return

    except Exception as e:
        print(f"Error reading arguments: {e}")
        return
    
    return

if __name__ == "__main__":
    main()