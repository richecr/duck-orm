from typing import List, Union


class Condition:
    field: str
    operator: str
    value: Union[List, str, int]

    def __init__(self, field: str, operator: str, value: Union[List, str, int]):
        self.field = field
        self.operator = operator
        self.value = value

    def get_condition(self):
        value = ''
        if (type(self.value) == str):
            value = "'{value}'".format(value=self.value)
        elif (type(self.value) == int):
            value = self.value
        elif (type(self.value == List)):
            if (self.operator != 'IN'):
                raise Exception(
                    'If the type of the value is List, then the operator must be IN')
            value = self.value
        else:
            raise Exception('Value type is not supported')

        return "{field} {operator} {value}".format(field=self.field, operator=self.operator, value=value)
