import logging

import xair_api

logging.basicConfig(level=logging.DEBUG)


def main():
    with xair_api.connect("XR18", ip="mixer.local") as mixer:
        for send in mixer.strip[0].send:
            send.level = -22.8

        mixer.strip[15].send[0].level = -16.3
        mixer.auxreturn.send[0].level = -15.3
        mixer.fxreturn[0].send[0].level = -14.3


if __name__ == "__main__":
    main()
