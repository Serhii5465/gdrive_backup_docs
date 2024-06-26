import wmi
from src import constants

def get_mnt_point():
    uuid_src = [
        constants.UUID_DELL_HDD,
        constants.UUID_MSI_HDD
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