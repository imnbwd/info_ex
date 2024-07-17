class Result:
    """错误信息"""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.success = code == 10000

    def to_dict(self):
        return {
            'code': self.code,
            'success': self.success,
            'message': self.message
        }
