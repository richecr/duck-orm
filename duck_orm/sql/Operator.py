from duck_orm.Exceptions.OperatorException import OperatorException


class Operator:
    operator: str

    def __init__(self, operator: str):
        if operator == '=':
            self.operator = '='
        elif operator == '<=':
            self.operator = '<='
        elif operator == '>=':
            self.operator = '>='
        elif operator == '>=':
            self.operator = '>='
        elif operator == 'LIKE':
            self.operator = 'LIKE'
        elif operator == 'NOT IN':
            self.operator = 'NOT IN'
        elif operator == 'IN':
            self.operator = 'IN'
        else:
            raise OperatorException(
                "Operator: {op} is invalid.".format(op=operator))
