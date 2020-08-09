import os

HOMEDIR = os.path.join(os.environ["HomeDrive"], os.environ["HomePath"])

# Global logging format
LOGGING_FORMAT = "%(asctime)s %(message)s"

# Defaults for the configuration file.
DEFAULT_CONFIG_PATH = os.path.join(HOMEDIR, ".eso_set_permutations")
