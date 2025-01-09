import wmi
from src import constants

def get_mnt_point():
    try:
        c = wmi.WMI()
        
        for i in c.Win32_LogicalDisk():
            if i.VolumeSerialNumber and i.VolumeSerialNumber.strip() == constants.UUID_SRC_DRIVE:
                return i.DeviceID + '\\'
        
        print("UUID not found")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None