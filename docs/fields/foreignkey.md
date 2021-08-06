# ForeignKey

This field is to represent the Foreign Key.
Let's look at some methods this field allows.

- The interface of a field `ForeignKey`:

``` python
ForeignKey(model: Type[Model], name_in_table_fk: str, unique: bool = False):
```

- Parameters:
    - `model`: The `Model` that will be used in the relationship.
    - `name_in_table_fk`: The name of the attribute that will be `FK` in 
    the other model.
    - `unique`: Whether this field is going to be a single value or not.

## Examples

Since this field is used to create some types of relationships, the examples
of use of this field can be found in the documentation on 
[OneToMany](./one_to_many.md) and [ManyToMany](./many_to_many.md).