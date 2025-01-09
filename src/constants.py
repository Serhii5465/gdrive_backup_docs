from os import path
from src import mnt

UUID_SRC_DRIVE = '00A559C0'

ROOT_REMOTE_DIR = 'gdrive:'

NAME_SYNC_DIR = 'gdrive_share'

MNT_POINT_SRC = mnt.get_mnt_point()

RCLONE_CONF_FILE = path.join(MNT_POINT_SRC, 'system', 'local', 'rclone', 'rclone.conf')

RCLONE_LOGS_DIR = path.join(MNT_POINT_SRC, 'logs', 'rclone_gdrive_documents')

PATH_SYNC_DIR = path.join(MNT_POINT_SRC, NAME_SYNC_DIR)