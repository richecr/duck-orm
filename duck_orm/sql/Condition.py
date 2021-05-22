from typing import List, Union

from duck_orm.sql.Operator import Operator


class Condition:
    _field: str
    _operator: Operator
    _value: Union[List, str, int]
    _lower_str: bool

    def __init__(self, field: str, operator: str, value: Union[List, str, int], lower_str: bool = False):
        self._field = field
        self._operator = Operator(operator)
        self._value = value
        self._lower_str = lower_str

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

        field = self._field
        if (self._lower_str):
            field = 'LOWER({field})'.format(field=field)
            value = "LOWER('{value}')".format(value=self._value)

        return "{field} {operator} {value}".format(field=field, operator=self._operator.operator, value=value)
