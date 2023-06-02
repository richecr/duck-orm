class Query:
    def __init__(self, name_table: str) -> None:
        self.name_table = name_table

    def select(self, fields: list[str]):
        return Query(select_fields=fields)


from sqlalchemy import column, text
from sqlalchemy.sql.expression import select

print(
    select(column("user.id"), column("user.name"))
    .where((column("user.id") == text("1")) & column("user.id").between(1, 2))
    .limit(10)
    .order_by(column("user.name").asc())
)
