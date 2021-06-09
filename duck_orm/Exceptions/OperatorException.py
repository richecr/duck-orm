class OperatorException(Exception):
    def __init__(self, *args, **kwargs):
        super(OperatorException, self).__init__(*args, **kwargs)
