# OneToOne

This field is to represent the One To One relationship.
Let's look at some methods this field allows.

- The interface of a field `OneToOne`:

``` python
OneToOne(model: Model, name_relation: str):
```

- Parameters:
    - `model`: The `Model` that will be used in the relationship.
    - `name_relation`: The name of the attribute that will be `FK` in 
    the other model.

## Examples

Os exemplos para esse tipo de relacionamentos podem ser encontrados [aqui](./relations.md#onetoone)