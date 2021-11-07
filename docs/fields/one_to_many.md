# OneToMany

This field is to represent the One to Many relationship.
Let's look at some methods this field allows.

- The interface of a field `OneToMany`:

``` python
OneToMany(model: Model, name_in_table_fk: str):
```

- Parameters:
    - `model`: The other `Model` that will be used in the relationship.
    - `name_in_table_fk`: The name of the attribute that will be `FK` in 
    the other template.

## Methods

Methods that are supported by the ManyToMany field.

### add

Método que deve ser chamado de uma instância do modelo da lado do 
relacionamento N.

```python
async def add(model: Type[Model]) -> Model:
```

- Parameters:
    - `model`: An instance of the `Model` of the relation.

## Examples

First, let's create our models.

Examples of using the methods explained above.

``` python
class City(Model):
    __tablename__ = 'cities'
    __db__ = db
    model_manager = model_manager

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    name: str = Field.String(unique=True)

    @classmethod
    def relationships(cls):
        cls.persons = OneToMany(
            model=Person,
            name_in_table_fk='city')

class Person(Model):
    __tablename__ = 'persons'
    __db__ = db
    model_manager = model_manager

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger()
    salary: int = Field.BigInteger()

    @classmethod
    def relationships(cls):
        cls.city: City = ForeignKey(
            model=City,
            name_in_table_fk='id',
            name_constraint='person_city_fk')
```

Now let's save a city and a person and then list the people of a
certain city:

``` python hl_lines="5 7 10 11 13-14"
await model_manager.create_all_tables()

city_cg = City(name="Campina Grande")
person_1 = Person(
    first_name="Rich", last_name="Carvalho", age=22, salary=1250, city=city_cg)
person_2 = Person(
    first_name="Elton", last_name="Carvalho", age=25, salary=1450, city=city_cg)

city_cg = await City.save(city_cg)
person_1 = await City.persons.add(person_1)
person_2 = await City.persons.add(person_2)

# Return all the people in this city
persons: list[Person] = await City.persons.get_all()

for person in persons:
    print(person.first_name)  # Rich and Elton
    print(person.city.name)  # Campina Grande and Campina Grande
```

On lines 8 and 9 we are saving two people from the city of Campina Grande.
And on line 11, I list the people in that city (they have
relationship with that city).

We also have the `add` method in the `OneToMany` field:

``` python hl_lines="4"
person_3 = Person(
    first_name="Lucas", last_name="Andrade", age=22, salary=1145)

person_3: Person = await city_cg.persons.add(person_3)
```

With that I can save a person and I already add in the city that
I want to.