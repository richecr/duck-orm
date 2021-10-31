# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [1.0.0] - 10-31-2021: Not Released

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