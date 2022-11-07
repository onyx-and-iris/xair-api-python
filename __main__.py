import xair_api


def main():
    kind_id = "XR18"
    ip = "<ip address>"

    with xair_api.connect(kind_id, ip=ip) as mixer:
        mixer.strip[8].config.name = "sm7b"
        mixer.strip[8].config.on = True
        print(
            f"strip 09 ({mixer.strip[8].config.name}) has been set to {mixer.strip[8].config.on}"
        )


if __name__ == "__main__":
    main()
