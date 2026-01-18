# Create application manager for handling which application is determined to run.
# Adjust applications so that arguments are passed after the application is created.

class Application:
    def __init__(self, application: str):
        self.application = application

    def run(self) -> None:
        raise RuntimeError(f"run method was not implemanted for \"{self.application}\" application")
