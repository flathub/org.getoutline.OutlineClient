#!/usr/bin/python3
import configparser
import errno
import fnmatch
import os
import os.path
import shutil
import subprocess
import sys
from pathlib import Path

FLATPAK_INFO = "/.flatpak-info"

# https://github.com/flathub/com.valvesoftware.Steam/blob/19c758cc4b8c09db27fb9c1bc4fea2b70aff141f/steam_wrapper/steam_wrapper.py#L101


def read_flatpak_info(path):
    flatpak_info = configparser.ConfigParser()
    with open(path) as f:
        flatpak_info.read_file(f)
    return {
        "flatpak-version": flatpak_info.get("Instance", "flatpak-version"),
        "runtime": flatpak_info.get("Application", "runtime"),
        "runtime-path": flatpak_info.get("Instance", "runtime-path"),
        "app-path": flatpak_info.get("Instance", "app-path"),
        "app-extensions": dict((s.split("=")
                                for s in flatpak_info.get("Instance", "app-extensions",
                                                          fallback="").split(";") if s)),
        "runtime-extensions": dict((s.split("=")
                                   for s in flatpak_info.get("Instance", "runtime-extensions",
                                                             fallback="").split(";") if s)),
        "filesystems": flatpak_info.get("Context", "filesystems",
                                        fallback="").split(";")
    }


def main():
    os.chdir(os.environ["HOME"])  # Ensure sane cwd
    current_info = read_flatpak_info(FLATPAK_INFO)

    print(current_info)

    outline_proxy_controller_path = Path(
        f"{current_info['app-path']}/outline-client/resources/app.asar.unpacked/tools/outline_proxy_controller/dist")
    install_linux_service_script_path = outline_proxy_controller_path / \
        "install_linux_service.sh"

    command = ["/usr/bin/flatpak-spawn", "--host", "--clear-env", "pkexec",
               install_linux_service_script_path, outline_proxy_controller_path]

    os.execv(command[0], command)


if __name__ == '__main__':
    main()
