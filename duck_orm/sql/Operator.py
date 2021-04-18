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
        elif operator == 'NOT IN':
            self.operator = 'NOT IN'
        elif operator == 'IN':
            self.operator = 'IN'
