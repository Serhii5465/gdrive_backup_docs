import sys
import wmi
from pathlib import Path
from typing import Union

def UUID_DELL_HDD() -> str:
    return '5837B806'

def UUID_MSI_HDD() -> str:
    return '7E0E4F54'

def MOUNT_POINTS() -> Union[str, None]:
    uuid_src = [
        UUID_DELL_HDD(),
        UUID_MSI_HDD()
    ]

    try:
        c = wmi.WMI()
        
        for i in c.Win32_LogicalDisk():
            for j in uuid_src:
                if i.VolumeSerialNumber and i.VolumeSerialNumber.strip() == j:
                    return i.DeviceID + '\\'
        
        print("UUID not found")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def RCLONE_CONF_FILE() -> str:
    return str("E:\\local\\rclone\\rclone.conf")

def ROOT_REMOTE_DIR() -> str:
    return 'google-drive:'

def ROOT_LOCAL_DIR() -> str:
    return 'gdrive_share'