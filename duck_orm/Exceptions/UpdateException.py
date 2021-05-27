class UpdateException(Exception):
    def __init__(self, *args, **kwargs):
        super(UpdateException, self).__init__(*args, **kwargs)
