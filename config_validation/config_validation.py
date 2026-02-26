from collections import Counter


class ConfigValidation:
    REQUIRED_KEYS = {
        "width",
        "height",
        "entry",
        "exit",
        "output_file",
        "perfect",
    }

    OPTIONAL_KEYS = {"seed"}

    def __init__(self, filename):
        self.filename = filename

    def validate(self):
        if not self.filename.endswith(".txt"):
            raise ValueError("Input file must be a .txt file")

        with open(self.filename, "r") as f:
            lines = f.readlines()

        config = {}

        # Remove comments and empty lines
        clean_lines = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            clean_lines.append(line)

        if len(clean_lines) < len(self.REQUIRED_KEYS):
            raise ValueError("Missing required configuration keys")

        # Check duplicates
        keys = [line.split("=")[0].strip().lower() for line in clean_lines]
        counts = Counter(keys)
        for key, count in counts.items():
            if count > 1:
                raise ValueError(f"Duplicate key found: {key}")

        for line in clean_lines:
            if "=" not in line or line.count("=") != 1:
                raise ValueError("Each line must contain exactly one '='")
            if " " in line:
                raise ValueError("No spaces allowed in key-value pairs")
            key, value = line.split("=")
            key = key.strip().lower()
            value = value.strip()

            if key not in self.REQUIRED_KEYS and key not in self.OPTIONAL_KEYS:
                raise ValueError(f"Invalid key: {key}")

            if key == "width":
                config["width"] = int(value)

            elif key == "height":
                config["height"] = int(value)

            elif key == "entry":
                config["entry"] = tuple(map(int, value.split(",")))

            elif key == "exit":
                config["exit"] = tuple(map(int, value.split(",")))

            elif key == "seed":
                config["seed"] = int(value)

            elif key == "output_file":
                if not value.endswith(".txt"):
                    raise ValueError("Output file must be .txt")
                config["output_file"] = value

            elif key == "perfect":
                if value.lower() not in {"true", "false"}:
                    raise ValueError("Perfect must be 'true' or 'false'")
                config["perfect"] = value.lower()

        # Check required keys exist
        missing = self.REQUIRED_KEYS - config.keys()
        if missing:
            raise ValueError(f"Missing required keys: {missing}")

        return config
