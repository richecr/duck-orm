# Fields

So far we only have 5 types available and 5 special types: `ForeignKey`, 
`OneToMany`, `ManyToOne`, `OneToOne` and `ManyToMany`.

These special types are for relationships between database tables.

!!! tip
    Para mais detalhes sobre os campos de relacionamento, consulte [aqui](./relationships.md)

## Common Types:

### String

``` python
String(
    unique: bool = False, primary_key: bool = False, not_null: bool = False,
    default_value = None
)
```

- Type in database postgres: `TEXT`
- Type in database sqlite: `TEXT`
- Type: `str`

### Integer

``` python
Integer(
    min_value: int = None, unique: bool = False, primary_key: bool = False,
    auto_increment: bool = False, not_null: bool = False, default_value = None
)
```

- Type in database postgres: `INTEGER`
- Type in database sqlite: `INTEGER`
- Type: `int`

### BigInteger

``` python
BigInteger(
    unique: bool = False, primary_key: bool = False, default_value = None
)
```

- Type in database postgres: `BIGINT`
- Type in database sqlite: `BIGINT`
- Type: `int`

### Varchar

``` python
Varchar(
    length: int, unique: bool = False, primary_key: bool = False,
    default_value = None
)
```

- Type in database postgres: `VARCHAR`
- Type in database sqlite: `VARCHAR`
- Type: `str`

### Boolean

``` python
Boolean(not_null: bool = False, default_value = None)
```

- Type in database postgres: `BOOLEAN`
- Type in database sqlite: `INTEGER`
- Type: `bool`
