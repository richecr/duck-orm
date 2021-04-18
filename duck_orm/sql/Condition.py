from typing import List, Union

from duck_orm.sql.Operator import Operator


class Condition:
    _field: str
    _operator: Operator
    _value: Union[List, str, int]

    def __init__(self, field: str, operator: str, value: Union[List, str, int]):
        self._field = field
        self._operator = Operator(operator)
        self._value = value

    def get_condition(self):
        value = ''
        if (type(self._value) == str):
            value = "'{value}'".format(value=self._value)
        elif (type(self._value) == int):
            value = self._value
        elif (type(self._value == List)):
            if (self._operator.operator != 'IN'):
                raise Exception(
                    'If the type of the value is List, then the operator must be IN')
            value = self._value
        else:
            raise Exception('Value type is not supported')

        return "{field} {operator} {value}".format(field=self._field, operator=self._operator.operator, value=value)
