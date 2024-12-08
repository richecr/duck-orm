class OperatorException(Exception):
    def __init__(self, *args, **kwargs):
        super(OperatorException, self).__init__(*args, **kwargs)


class UpdateException(Exception):
    def __init__(self, *args, **kwargs):
        super(UpdateException, self).__init__(*args, **kwargs)


class IdInvalidException(Exception):
    def __init__(self, *args, **kwargs):
        super(IdInvalidException, self).__init__(*args, **kwargs)
