import threading
from logging import config

import obsws_python as obsws

import xair_api

config.dictConfig(
    {
        'version': 1,
        'formatters': {
            'standard': {
                'format': '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'
            }
        },
        'handlers': {
            'stream': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
            }
        },
        'loggers': {
            'xair_api.xair': {
                'handlers': ['stream'],
                'level': 'DEBUG',
                'propagate': False,
            }
        },
        'root': {'handlers': ['stream'], 'level': 'WARNING'},
    }
)


class Observer:
    def __init__(self, mixer, stop_event):
        self._mixer = mixer
        self._stop_event = stop_event
        self._client = obsws.EventClient()
        self._client.callback.register(
            (
                self.on_current_program_scene_changed,
                self.on_exit_started,
            )
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.disconnect()

    def on_current_program_scene_changed(self, data):
        scene = data.scene_name
        print(f'Switched to scene {scene}')
        match scene:
            case 'START':
                print('Toggling strip 01 on')
                self._mixer.strip[0].mix.on = not self._mixer.strip[0].mix.on
            case 'BRB':
                print('Setting strip 08 fader')
                self._mixer.strip[7].mix.fader = -12.8
            case 'END':
                print('Settings strip 02 color')
                self._mixer.strip[1].config.color = 8
            case 'LIVE':
                self._mixer.config.mute_group[0].on = True
                print(f'Mute Group 1 is {self._mixer.config.mute_group[0].on}')

    def on_exit_started(self, _):
        self._stop_event.set()


def main():
    with xair_api.connect('MR18', ip='mixer.local') as mixer:
        stop_event = threading.Event()

        with Observer(mixer, stop_event):
            stop_event.wait()


if __name__ == '__main__':
    main()
