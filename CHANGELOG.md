# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.2.0] - 2021-10-10: Not Released

### Added
- Added the `on_delete` parameters to the `ForeignKey` field.
- Added doc of parameter `on_delete` to the `ForeignKey` field.
- Added the `on_update` parameters to the `ForeignKey` field.
- Added doc of parameter `on_update` to the `ForeignKey` field.
- Implement Method `find_by_id`.
- Add parameter `name_constraint` in `ForeignKey` field.
- Added doc of parameter `name_constraint` to the `ForeignKey` field.

### Corretion
- Documentation fix: portuguese words and some broken links.

## [0.1.0] - 2021-08-06

### Added
- Launch.
- Creation of models.
- Support for postgresql and sqlite.
- Supported Fields: String, Integer, BigInteger, Varchar and Boolean.
- Supported Relationships: One To One, One To Many and Many To Many.