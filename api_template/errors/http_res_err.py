class HttpResException(Exception):
    def __init__(self, message: str, code: str, detail :str = None):
        self.msg = message
        self.code = code
        self.detail =  detail