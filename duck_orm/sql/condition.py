from typing import List, Union

from duck_orm.exceptions import OperatorException
from duck_orm.sql.operator import Operator


class Condition:
    def __init__(
        self,
        field: str,
        operator: str,
        value: Union[List, str, int],
        lower_str: bool = False,
    ):
        self._field = field
        self._operator = Operator(operator)
        self._value = value
        self._lower_str = lower_str

    def get_condition(self):
        value = ""
        if isinstance(self._value, str):
            value = "'{value}'".format(value=self._value)
        elif isinstance(self._value, int):
            value = self._value
        elif isinstance(self._value, List):
            if self._operator.operator != "IN":
                raise OperatorException("If the type of the value is List, then the operator must be IN")
            value = "(" + ", ".join(list(map(lambda x: f"'{x}'", self._value))) + ")"
        else:
            raise OperatorException("Value type is not supported")

        field = self._field
        if self._lower_str:
            field = "LOWER({field})".format(field=field)
            value = "LOWER('{value}')".format(value=self._value)
        return "{field} {operator} {value}".format(field=field, operator=self._operator.operator, value=value)
