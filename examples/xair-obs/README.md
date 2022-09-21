## Requirements

-   [OBS Studio](https://obsproject.com/)
-   [OBS Python SDK for Websocket v5](https://github.com/aatikturk/obsws-python)

## About

A simple demonstration showing how to sync XAir states with OBS scene switches. The script assumes you have OBS connection info saved in
a config file named `config.toml` placed next to `__main__.py`. It also assumes you have scenes named `START` `BRB` `END` and `LIVE`.

A valid `config.toml` file might look like this:

```toml
[connection]
host = "localhost"
port = 4455
password = "mystrongpass"
```

## Use

Change the xair ip argument from `mixer.local` to the ip of your xair mixer. Run the code and switch between scenes in OBS.

## Notes

This example was inspired by [OBS-to-XAir](https://github.com/lebaston100/OBS-to-XAir)
