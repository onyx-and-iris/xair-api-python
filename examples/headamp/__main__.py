# Warning this script enables the phantom power for strip 09

import logging

import xair_api

logging.basicConfig(level=logging.DEBUG)


def main():
    with xair_api.connect("XR18", ip="mixer.local") as mixer:
        mixer.headamp[8].phantom = True
        for i in range(-12, -6):
            mixer.headamp[8].gain = i
            print(mixer.headamp[8].gain)
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
