# Methods

Aqui vamos mostrar alguns métodos que o `Model` possui e também vamos ver como
usar cada um deles.

**Para executar os exemplos executem usando o `ipython`.**

## get_name

Método que retorna o nome do `Model` no banco de dados.

E caso, o atributo `__tablename__` não tenha sido atribuído no `Model`, então
esse método irá retornar o nome da classe em caixa baixa.

``` python hl_lines="7 16"
class Person(Model):
    __db__ = db

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)

Person.get_name() # will return 'person'.

class Client(Model):
    __tablename__ = 'clients'
    __db__ = db

    # definitions of fields
    ...

Client.get_name() # Will return 'clients'.
```

## create

Método assíncrono que irá criar a tabela que representa o `Model` no banco de dados.

Ele sempre deve ser usado **antes** de tentar salvar, buscar ou deletar algum objeto
do `Model`.

``` python hl_lines="11"
class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()

await Person.create()
```

## save

``` python
save(model: Model) -> Model:
```

Método assíncrono que irá salvar um objeto na tabela no banco de dados.

- Parâmetros:
    - `model`: Instância do `Model` com os campos preenchidos.

``` python
...

person_1 = Person(
    first_name="Teste 1", last_name="teste lastname", age=19, salary=5000)
person_2 = Person(
    first_name="Teste 2", last_name="teste lastname", age=25, salary=4000)
person_3 = Person(
    first_name="Teste 3", last_name="teste lastname", age=22, salary=2500)

person_1 = await Person.save(person_1)
person_2 = await Person.save(person_2)
person_3 = await Person.save(person_3)

person_1.id # 1
person_1.first_name # Teste 1
person_1.age # 19

person_2.id # 2
person_2.first_name # Teste 2
person_2.age # 25

person_3.id # 3
person_3.first_name # Teste 3
person_3.age # 22

```

## find_all

``` python
find_all(
    fields_includes: List[str] = [],
    fields_excludes: List[str] = [],
    conditions: List[Condition] = [],
    limit: int = None
) -> List[Model]
```

Método assíncrono que recupera todos os objetos persistidos em uma tabela no
banco de dados.

- Parâmetros:
    - `fields_includes`: Os campos do `Model` que devem ser recuperados.
    - `fields_excludes`: Os campos do `Model` que não devem ser recuperados.
    - `conditions`: As condições para filtrar os objetos.
    - `limit`: O limite máximo de objetos que devem ser recuperados.

``` python
...

from duck_orm.sql.condition import Condition

persons: list[Person] = await Person.find_all(
    fields_includes = ['first_name', 'age', 'salary],
    # Poderia ter deixado esse parâmetro em branco, pois ele já não está no
    # fields_includes.
    fields_excludes = ['id'],
    conditions = [
        Condition('first_name', 'LIKE', 'Teste'),
        Condition('salary', '>=', 2500)
    ],
    limit = 2
)

for person in persons:
    print(person.id) # None em todos.
    print(person.first_name) # Teste 2, Teste 3
    print(person.age) # 25, 22
    print(person.salary) # 5000, 2500
```
