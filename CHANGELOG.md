# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Before any major/minor/patch bump all unit tests will be run to verify they pass.

## [Unreleased]

-   [x]

## [2.0.0] - 2022-11-07

Some support for the X32 mixer has been added using an adapter module but the code related to the XAir api has been left largely untouched.
However, a couple of changes have been made which are breaking, they are as follows:

### Changed

-   FX class added to fx module. This now deals with osc addresses that begin with "/fx/". Call it with mixer.fx.
-   FxRtn class added to rtn module. This now deals with addresses that begin with "/rtn/". Call it with mixer.fxreturn
-   Aux class renamed to AuxRtn in rtn module. Call it with mixer.auxreturn.

These changes were made to better resemble the underlying osc api and to better describe the function of the classes.

### Added

-   A small number of X32 tests. More will be added. XAir tests moved into it's own test module.
-   XAirRemote lower level section added to README.
-   Links to OSC command documentation added to README.

### Removed

-   mixer.aux was renamed to mixer.auxreturn

## [1.1.0] - 2022-09-05

### Added

-   tomli/tomllib compatibility layer to support python 3.10

## [1.0.2] - 2022-08-07

### Added

-   now packaged with poetry
-   package added to pypi
-   pypi, isort badges added to readme

### Changed

-   package renamed to xair-api
-   now using tomllib for config, requires python 3.11
-   readme, example updated.
-   imports isorted.

## [0.1.0] - 2022-05-01

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

## [0.0.1] - 2022-04-05

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
