from yaml import load, CLoader as Loader

def parse_yaml (file: str = "config.yaml") -> None:
    try: 
        with open(file, "r") as f:
            config = load(f, Loader = Loader)
            return config["telegram"]["token"]
    except FileNotFoundError:
        print("File not found")
        return None
