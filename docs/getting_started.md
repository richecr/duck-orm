# Getting Started

## Installation

```bash
$ pip install duck-orm
```

### Dependencies

DuckORM uses `databases` for database connection.

### Extras dependencies

DuckORM has 3 dependencies that depend on the backend database you want to use:

#### Postgresql

```bash
$ pip install duck-orm[postgresql]
```

Will install also `asyncpg`.

#### Postgresql + aiopg

```bash
$ pip install duck-orm[postgresql+aiopg]
```

Will install also `aiopg`.

#### SQLite

```bash
$ pip install duck-orm[sqlite]
```

Will install also `aiosqlite`.

### Install dependencies manually

Se desejar, pode instalar as dependências manualmente também.

Exemplo:

```bash
$ pip install asyncpg
```