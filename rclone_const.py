import sys
from pathlib import Path
from cyg_mnt_point import mnt 

def UUID_DELL_HDD() -> str:
    return '345837F85837B806'

def UUID_MSI_HDD() -> str:
    return '347E0E947E0E4F54'

def MOUNT_POINTS() -> str:
    uuid_src = [
        UUID_DELL_HDD(),
        UUID_MSI_HDD()
    ]
    
    mnt_point = ''
    
    for i in uuid_src:
        mnt_point = mnt.get_cygwin_mount_point(i)
        if mnt_point is not None:
            return mnt_point
    
    if mnt_point is None:
        sys.exit('Source HDD did not mount')

def RCLONE_CONF_FILE() -> str:
    return str(Path.home()) + '/.config/rclone/rclone.conf'

def ROOT_REMOTE_DIR() -> str:
    return 'google-drive:'

def ROOT_LOCAL_DIR() -> str:
    return 'gdrive_share'