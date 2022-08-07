import xair_api


def main():
    with xair_api.connect(kind_id, ip=ip) as mixer:
        mixer.strip[8].config.name = "sm7b"
        mixer.strip[8].config.on = True
        print(
            f"strip 09 ({mixer.strip[8].config.name}) has been set to {mixer.strip[8].config.on}"
        )


if __name__ == "__main__":
    kind_id = "MR18"
    ip = "<ip address>"

    main()
