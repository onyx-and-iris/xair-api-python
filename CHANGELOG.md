# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Before any major/minor/patch patch is released all test units will be run to verify they pass.

## [Unreleased]

-   [ ]

## [0.1.0] - 2021-05-01

### Added

-   kind maps for "XR16", "XR12" added.
-   get() added to kind module.
-   pre-commit.ps1 added for use with git hook.
-   tests passed badge added to readme.

### Changed

-   readme updated to reflect changes.

### Fixed

-   link to clone repo fixed in readme.
-   unit tests migrated from nose to pytest since nose will not be supported from python 3.10 onwards.

## [0.0.1] - 2021-04-05

### Added

-   \_query() added to base class, allows testing a single parameter.
-   Interface entry point defined.
-   Kind map for XR18/MR18 added
-   Higher level classes (lr, strip, bus, fxsend, aux, rtn) implemented
-   Subclass mixin implemented (shared classes)
-   meta module added
-   util module added, mostly functions that perform math operations.
-   readme initial commit.

### Changed

-   base class now supports context manager.
-   load ip from ini
-   unit tests initial commit. tests for shared classes added.
