# OneToOne

This field is to represent the One To One relationship.
Let's look at some methods this field allows.

- The interface of a field `OneToOne`:

``` python
OneToOne(
    model: Model,
    name_constraint: str = "",
    on_delete: ActionsEnum = ActionsEnum.NO_ACTION.value,
    on_update: ActionsEnum = ActionsEnum.CASCADE.value
):
```

- Parameters:
    - `model`: The `Model` that will be used in the relationship.
    - `name_constraint`: The name of the attribute that will be `FK` in 
    the other model.
    - `on_delete`: Action ON DELETE: `CASCADE`, `NO ACTION`, `RESTRICT`, 
    `SET DEFAULT` and `SET NULL`.
    - `on_update`: Action ON UPDATE: `CASCADE`, `NO ACTION`, `RESTRICT`, 
    `SET DEFAULT` and `SET NULL`.

## Examples

Examples for these types of relationships can be found [here](./relations.md#onetoone)