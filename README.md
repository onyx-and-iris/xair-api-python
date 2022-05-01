[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/onyx-and-iris/xair-api-python/blob/dev/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Tests Status](./tests/MR18.svg?dummy=8484744)

# Mair Remote

This package offers a python interface for the [Behringer XAir](https://www.behringer.com/series.html?category=R-BEHRINGER-XAIRSERIES), [Midas MR](https://www.midasconsoles.com/catalog.html?catalog=Category&category=C-MIDAS-MIXERS-DIGITALSTAGEBOXMIXERS) series of digital rack mixers. I only have access to an MR18 for testing so if there is an error in the kind maps feel free to raise an issue or PR.

## Prerequisites

-   Python 3.9+

## Installation

```
git clone https://github.com/onyx-and-iris/xair-api-python
cd xair-api-python
```

Just the interface:

```
pip install .
```

With development dependencies:

```
pip install -e .['development']
```

## Usage

### Connection

An ini file named config.ini, placed into the current working directory of your code may be used to configure the mixers ip. It's contents should resemble:

```
[connection]
ip=<ip address>
```

Alternatively you may state it explicitly as an argument to mair.connect()

### Example 1

```python
import mair

def main():
    with mair.connect(kind_id, ip=ip) as mixer:
        mixer.strip[8].config.name = 'sm7b'
        mixer.strip[8].config.on = True
        print(f'strip 09 ({mixer.strip[8].config.name}) has been set to {mixer.strip[8].config.on}')

if __name__ == '__main__':
    kind_id = 'MR18'
    ip = '<ip address>'

    main()
```

## API

Currently the following devices are support:

-   `XR18`
-   `MR18`
-   `XR16`
-   `XR12`

### MAirRemote (higher level)

`mixer.lr`

A class representing Main LR channel

`mixer.strip`

A Strip tuple containing a class for each input strip channel

`mixer.bus`

A Bus tuple containing a class for each output bus channel

`mixer.dca`

A DCA tuple containing a class for each DCA group

`mixer.fxsend`

An FXSend tuple containing a class for each FX Send channel

`mixer.fxreturn`

An FXReturn tuple containing a class for each FX Return channel

`mixer.aux`

A class representing aux channel

`mixer.rtn`

An RTN tuple containing a class for each rtn channel

`mixer.config`

A class representing the main config settings

### `LR`

Contains the subclasses:
(`Config`, `Dyn`, `Insert`, `EQ`, `Mix`)

### `Strip`

Contains the subclasses:
(`Config`, `Preamp`, `Gate`, `Dyn`, `Insert`, `GEQ`, `EQ`, `Mix`, `Group`, `Automix`)

### `Bus`

Contains the subclasses:
(`Config`, `Dyn`, `Insert`, `EQ`, `Mix`, `Group`)

### `FXSend`

Contains the subclasses:
(`Config`, `Mix`, `Group`)

### `Aux`

Contains the subclasses:
(`Config`, `Preamp`, `EQ`, `Mix`, `Group`)

### `Rtn`

Contains the subclasses:
(`Config`, `Preamp`, `EQ`, `Mix`, `Group`)

### `Subclasses`

For each subclass the corresponding properties are available.

`Config`

-   `name`: string
-   `color`: int, from 0, 16
-   `inputsource`: int
-   `usbreturn`: int

`Preamp`

-   `on`: bool
-   `usbtrim`: float, from -18.0 to 18.0
-   `usbinput`: bool
-   `invert`: bool
-   `highpasson`: bool
-   `highpassfilter`: int, from 20 to 400

`Gate`

-   `on`: bool
-   `mode`: str, one of ('gate', 'exp2', 'exp3', 'exp4', 'duck')
-   `threshold`: float, from -80.0 to 0.0
-   `range`: int, from 3 to 60
-   `attack`: int, from 0 to 120
-   `hold`: float, from 0.02 to 2000
-   `release`: int, from 5 to 4000
-   `keysource`, from 0 to 22
-   `filteron`: bool
-   `filtertype`: int, from 0 to 8
-   `filterfreq`: float, from 20 to 20000

`Dyn`

-   `on`: bool
-   `mode`: str, one of ('comp', 'exp')
-   `det`: str, one of ('peak', 'rms')
-   `env`: str, one of ('lin', 'log')
-   `threshold`: float, from -60.0 to 0.0
-   `ratio`: int, from 0 to 11
-   `knee`: int, from 0 to 5
-   `mgain`: float, from 0.0 to 24.0
-   `attack`: int, from 0 to 120
-   `hold`: float, from 0.02 to 2000
-   `release`: int, from 5 to 4000
-   `mix`: int, from 0 to 100
-   `keysource`: int, from 0 to 22
-   `auto`: bool
-   `filteron`: bool
-   `filtertype`: int, from 0 to 8
-   `filterfreq`: float, from 20 to 20000

`Insert`

-   `on`: bool
-   `sel`: int

`GEQ`
The following method names preceded by `slider_`

-   `20`, `25`, `31_5`, `40`, `50`, `63`, `80`, `100`, `125`, `160`,
-   `200`, `250`, `315`, `400`, `500`, `630`, `800`, `1k`, `1k25`, `1k6`, `2k`,
-   `2k5`, `3k15`, `4k`, `5k`, `6k3`, `8k`, `10k`, `12k5`, `16k`, `20k`: float, from -15.0 to 15.0

for example: `slider_20`, `slider_6k3` etc..

`EQ`

-   `on`: bool
-   `mode`: str, one of ('peq', 'geq', 'teq')

For the subclasses: `low`, `low2`, `lomid`, `himid`, `high2`, `high` the following properties are available:

-   `type`: int, from 0 to 5
-   `frequency`: float, from 20.0 to 20000.0
-   `gain`: float, -15.0 to 15.0
-   `quality`: float, from 0.3 to 10.0

for example: `eq.low2.type`

`Mix`

-   `on`: bool
-   `fader`: float, -inf, to 10.0
-   `lr`: bool

`Group`

-   `dca`: int, from 0 to 15
-   `mute`: int, from 0 to 15

`Automix`

-   `group`: int, from 0 to 2
-   `weight`: float, from -12.0 to 12.0

### `DCA`

-   `on`: bool
-   `name`: str
-   `color`: int, from 0 to 15

### `Config`

The following method names preceded by `chlink`

-   `1_2`, `3_4`, `5_6`, `7_8`, `9_10`, `11_12`, `13_14`, `15_16`

The following method names preceded by `buslink`

-   `1_2`, `3_4`, `5_6`

for example: `chlink1_2`, `buslink5_6` etc..

-   `link_eq`: bool
-   `link_dyn`: bool
-   `link_fader_mute`: bool
-   `amixenable`: bool
-   `amixlock`: bool
-   `mute_group`: bool

For the subclass `monitor` the following properties are available

-   `level`: float, -inf to 10.0
-   `source`: int, from 0 to 14
-   `chmode` bool
-   `busmode` bool
-   `dim` bool
-   `mono` bool
-   `mute` bool
-   `dimfpl` bool

for example: `config.monitor.chmode`

### `Tests`

People plug expensive equipment into these mixers, the unit tests adjust parameter values such as gain sliders etc. My advice is
to unplug all equipment from the mixer before running these tests. No tests alter phantom power state.
Save your current settings to a snapshot first.

First make sure you installed the [development dependencies](https://github.com/onyx-and-iris/xair-api-python#installation)

To run the tests from tests directory:

`pytest -v`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Special Thanks

[Peter Dikant](https://github.com/peterdikant) for writing the base class
