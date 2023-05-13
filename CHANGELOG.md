# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.2] - 13-05-2023: Released

### Added
- Added logs in methods using the lib `logging`.
- Added `ModelManager` to manage database tables.
- Preparing `DuckORM` to support migrations with [`duck-orm-cli`](https://github.com/richecr/duck-orm-cli).

### Corretion
- Method `associations` now ignores fields that are not of type `ForeingKey` or `OneToOne`.


## [1.0.1] - 11-06-2021: Released

### Added
- Added `__tablename__` attribute of models in ModelManager.

### Corretion
- ModelManager `create_all_tables` method does not create the tables
and neither the relationships already created, before it generated an error.
- The `drop_all_tables` to ModelManager method does not drop the tables
that do not exist, before it generated an error.
- Fixed the `add` and `get_all` method of the `OneToMany` field.
- Fixed the `add`, `add_models` and `get_all` method of the `ManyToMany` field.
- Fixed `parser` method of `QueryExecutor` module.


## [1.0.0] - 10-31-2021: Released

### Added
- Implement method `find_by_id` and documentation. #9 
- Added the `on_delete` parameters to the `ForeignKey` field and documentation. #17
- Added the `on_update` parameters to the `ForeignKey` field and documentation. #19 
- Add parameter `name_constraint` in `ForeignKey` field and documentation. #18 
- Add parameter `name_constraint` in `OneToOne` field and documentation. #30 
- Add `ManagerModel` and documentation. #31 
- Changed the way that the determined between the tables is created. #31 
- Add field Timestamp. #15
- Suport Databases 0.5.3.

### Corretion
- Documentation fix: portuguese words and some broken links.

## [0.1.0] - 08-06-2021

### Added
- Launch.
- Creation of models.
- Support for postgresql and sqlite.
- Supported Fields: String, Integer, BigInteger, Varchar and Boolean.
- Supported Relationships: One To One, One To Many and Many To Many.