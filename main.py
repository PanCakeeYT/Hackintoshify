from PySide6.QtWidgets import QApplication
from GUI_Screens.MainScreen import MainScreen, SettingsScreen, ConfigureKexts, CreateEFI, HelpandGuide, RepairEFI, SelectImage, Setup
import os


configuration_path_windows = "C:/ProgramData/Hackintoshify/config.ini"
SetupDetailsPathWindows = "C:/ProgramData/Hackintoshify/setup_details.json"
configuration_path_linux = "/etc/hackintoshify/config.ini"
SetupDetailsPathLinux = "/etc/hackintoshify/setup_details.json"
configuration_path_mac = "/Library/Application Support/Hackintoshify/config.ini"        # will be last because macOS is anoying.
SetupDetailsPathMac = "/Library/Application Support/Hackintoshify/setup_details.json"   # will be last because macOS is anoying.


# If files dont exist then create them
if not os.path.exists(configuration_path_windows):
    with open(configuration_path_windows, 'w') as f:
        f.write("[Settings]\ntheme=Dark\nverbose_logging=False\n")
        f.close()

if not os.path.exists(SetupDetailsPathWindows):
    with open(SetupDetailsPathWindows, 'w') as f:
        f.write("{}")
        f.close()

if not os.path.exists(configuration_path_linux):
    with open(configuration_path_linux, 'w') as f:
        f.write("[Settings]\ntheme=Dark\nverbose_logging=False\n")
        f.close()

if not os.path.exists(SetupDetailsPathLinux):
    with open(SetupDetailsPathLinux, 'w') as f:
        f.write("{}")
        f.close()

if not os.path.exists(configuration_path_mac):
    with open(configuration_path_mac, 'w') as f:
        f.write("[Settings]\ntheme=Dark\nverbose_logging=False\n")
        f.close()

if not os.path.exists(SetupDetailsPathMac):
    with open(SetupDetailsPathMac, 'w') as f:
        f.write("{}")
        f.close()


# If its users first time then open setup screen
def check_if_first_time():
    first_time = False
    if os.path.exists(SetupDetailsPathWindows):
        if os.path.getsize(SetupDetailsPathWindows) == 0:
            first_time = True
    elif os.path.exists(SetupDetailsPathLinux):
        if os.path.getsize(SetupDetailsPathLinux) == 0:
            first_time = True
    elif os.path.exists(SetupDetailsPathMac):
        if os.path.getsize(SetupDetailsPathMac) == 0:
            first_time = True
    return first_time


if __name__ == "__main__":
    app = QApplication([])

    main_screen = MainScreen()

    if check_if_first_time():
        setup_screen = Setup(parent=main_screen)
        setup_screen.show()
    else:
        main_screen.show()

    app.exec()