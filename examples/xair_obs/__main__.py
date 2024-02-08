import obsws_python as obs

import xair_api


class Observer:
    def __init__(self, mixer):
        self._mixer = mixer
        self._client = obs.EventClient()
        self._client.callback.register(self.on_current_program_scene_changed)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._client.disconnect()

    def on_current_program_scene_changed(self, data):
        scene = data.scene_name
        print(f"Switched to scene {scene}")
        match scene:
            case "START":
                print("Toggling strip 01 on")
                self._mixer.strip[0].mix.on = not self._mixer.strip[0].mix.on
            case "BRB":
                print("Setting strip 08 fader")
                self._mixer.strip[7].mix.fader = -12.8
            case "END":
                print("Settings strip 02 color")
                self._mixer.strip[1].config.color = 8
            case "LIVE":
                self._mixer.config.mute_group[0].on = True
                print(f"Mute Group 1 is {self._mixer.config.mute_group[0].on}")


def main():
    with xair_api.connect("MR18", ip="mixer.local") as mixer:
        with Observer(mixer):
            while _ := input("Press <Enter> to exit\n"):
                pass


if __name__ == "__main__":
    main()
