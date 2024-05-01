import os
import sys
from pathlib import Path
from cyg_mnt_point import mnt 

def DELL_INFO() -> dict[str, str]:
    return {
        'uuid' : '345837F85837B806',
        'docs' : '/cygdrive/d/documents/',
        'logs' : '/cygdrive/d/logs/'
    }

def MSI_INFO() -> dict[str, str]:
    return {
        'uuid' : '347E0E947E0E4F54',
        'docs' : '/cygdrive/e/documents/',
        'logs' : '/cygdrive/e/logs/'
    }

def MOUNT_POINTS() -> dict[str, str]:
    uuid_src = [
        DELL_INFO(),
        MSI_INFO()
    ]
    
    mnt_point = ''
    
    for i in uuid_src:
        mnt_point = mnt.get_cygwin_mount_point(i.get('uuid'))
        if mnt_point is not None:
            return i
    
    if mnt_point is None:
        sys.exit('Source HDD did not mount')

def RCLONE_CONF_FILE() -> str:
    return str(Path.home()) + '/.config/rclone/rclone.conf'

def ROOT_REMOTE_DIR() -> str:
    return 'google-drive:'