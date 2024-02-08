import logging

import xair_api

logging.basicConfig(level=logging.DEBUG)


def main():
    with xair_api.connect("XR18", ip="mixer.local") as mixer:
        for send in mixer.strip[0].send:
            send.level = -22.8

        mixer.strip[15].send[0].level = -16.5
        print(mixer.strip[15].send[0].level)

        mixer.auxreturn.send[0].level = -15.5
        print(mixer.auxreturn.send[0].level)

        mixer.fxreturn[0].send[0].level = -14.5
        print(mixer.fxreturn[0].send[0].level)


if __name__ == "__main__":
    main()
