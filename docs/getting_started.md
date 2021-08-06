# Getting Started

## Installation

```bash
pip install duck-orm
```

### Dependencies

`DuckORM` uses `databases` for database connection.

### Extras dependencies

`DuckORM` can have up to 3 dependencies according to the backend database(s) 
you want to use:

#### Postgresql

```bash
pip install duck-orm[postgresql]
```

Will install also `asyncpg`.

#### Postgresql + aiopg

```bash
pip install duck-orm[postgresql+aiopg]
```

Will install also `aiopg`.

#### SQLite

```bash
pip install duck-orm[sqlite]
```

Will install also `aiosqlite`.

### Install dependencies manually

If you wish, you can install the dependencies manually as well.

Example:

```bash
pip install asyncpg
```