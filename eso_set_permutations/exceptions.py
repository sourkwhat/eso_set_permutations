class NoConfigFileError(Exception):
    def __str__(self):
        return "No configuration file found, make one first!"
