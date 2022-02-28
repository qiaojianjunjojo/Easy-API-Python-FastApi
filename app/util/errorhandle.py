class InternalException(Exception):
    def __init__(self, code: str, desc: str):
        self.code = code
        self.desc = desc