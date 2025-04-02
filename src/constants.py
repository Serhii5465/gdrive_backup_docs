import os
from src import mnt

UUID_SRC_DRIVE = 'E46F39A2'

ROOT_REMOTE_DIR = 'gdrive:'

NAME_SYNC_DIR = 'gdrive_share'

MNT_POINT_SRC = mnt.get_mnt_point()

RCLONE_CONF_FILE = os.path.join(MNT_POINT_SRC, 'system', 'local', 'rclone', 'rclone.conf')

RCLONE_LOGS_DIR = os.path.join(os.environ["HOME"], 'logs', 'rclone_gdrive_documents')

PATH_SYNC_DIR = os.path.join(MNT_POINT_SRC, NAME_SYNC_DIR)