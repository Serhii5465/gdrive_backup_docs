from os import path
from src import mnt

UUID_DELL_HDD = '5837B806'

UUID_MSI_HDD = '7E0E4F54'

ROOT_REMOTE_DIR = 'google-drive:'

NAME_SYNC_DIR = 'gdrive_share'

MNT_POINT_SRC = mnt.get_mnt_point()

RCLONE_CONF_FILE = path.join(MNT_POINT_SRC, 'local', 'rclone', 'rclone.conf')

RCLONE_LOGS_DIR = path.join(MNT_POINT_SRC, 'logs', 'rclone_gdrive_documents')

PATH_SYNC_DIR = path.join(MNT_POINT_SRC, NAME_SYNC_DIR)